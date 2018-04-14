import tempfile
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from crimsononline.content.models import Contributor, Tag
from crimsononline.imageuploader.admin import BulkImageForm
from crimsononline.imageuploader.models import BulkImage

# from crimsononline.archive_photos.models import ArchiveImage


BulkImageFormset = modelformset_factory(BulkImage, form=BulkImageForm, extra=0)

###############################
# Upload destination handlers #
###############################


def handle_publishable(data):
    """Creates a new image object in admin from the form data"""
    pass


def handle_smugmug(data):
    """Uploads the image to smugmug"""
    pass


def handle_backup(data):
    """Uploads the image to S3"""
    pass


def get_image(data):
    # Initialize the boto S3 connection
    conn = S3Connection(settings.AWS_ACCESS_KEY_ID,
                        settings.AWS_SECRET_ACCESS_KEY)
    # Get the bucket for temporary images
    bucket = conn.get_bucket('temporary-uploads-thecrimson')

    k = Key(bucket)
    k.key = data['filename']

    # Read as a string and save the field
    image_data = k.get_contents_as_string()
    return SimpleUploadedFile(data['filename'], image_data)

#########
# Views #
#########


@login_required
def image_upload_form(request):
    # Get all contributors and tags
    contributors = Contributor.objects.filter(is_active=True)
    tags = Tag.objects.all()
    images = BulkImage.objects.admin_objects() \
        .filter(issue__issue_date__gte=datetime.now() - timedelta(days=-1))

    # Serialize to json
    json_contributors = serializers.serialize('json', contributors)
    json_tags = serializers.serialize('json', tags)

    data = {
        'bulk_formset': BulkImageFormset(),
        # Generate json serialized data for Javascript
        'json_contributors': json_contributors,
        'json_tags': json_tags,
        'images': images
    }
    return render(request, 'multi_image_upload.html', data)


@login_required
def image_metadata_submit(request):
    """
    Handles the user pressing "Save".

    Gets the submitted metadata and associates it with the temporary images
    based on file name.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('Accessed without POST.')
    formset = BulkImageFormset(request.POST, request.FILES)
    response = 'Successfully uploaded: <br/>'
    for form in formset:

        # Handle errors loudly
        if not form.is_valid():
            raise(Exception(form.errors))

        # Grab data from form
        data = form.cleaned_data
        response += data['filename'] + '<br/>'

        # By default, do not show in admin
        data['is_archiveimage'] = True

        # Load from the temporary S3 bucket
        image = get_image(data)

        # Admin handler
        if data['publishable']:
            data['is_archiveimage'] = False

        # Smugmug handlers

        # S3 backup handlers

        instance = form.save()
        instance.pic = image
        instance.save()
    return HttpResponse(response)


@login_required
def image_upload_target(request):
    """
    Handle multi-image uploads

    This handles the photos that are uploaded as soon as they are added. These
    are temporary photos that do not yet have associated metadata. This allows
    photos to upload while uploaders fill out their metadata.
    """

    # Basic error checking
    if request.method != 'POST':
        return HttpResponseBadRequest('Accessed without POST. No file data.')
    if not request.FILES:
        return HttpResponseBadRequest('No file data received')

    # Initialize the boto S3 connection
    conn = S3Connection(settings.AWS_ACCESS_KEY_ID,
                        settings.AWS_SECRET_ACCESS_KEY)
    # Get the bucket for temporary images
    bucket = conn.get_bucket('temporary-uploads-thecrimson')

    image_list = []
    # Iterate over all files we are receiving and upload to S3 temporarily
    # Note that the 'images' key corresponds to the input name in
    # multi_image_upload.html
    for image in request.FILES.getlist('images'):
        image_list.append(image.name)
        # Open a new tempfile (docs.python.org/2/library/tempfile.html)
        # Located on the server since direct S3 uploads aren't possible
        with tempfile.NamedTemporaryFile() as tmp:
            # Chucks allow for partial upload/resuming
            for chunk in image.chunks():
                tmp.write(chunk)
            # Writing changes seek location; reset for reading
            tmp.seek(0)
            # Create a key (S3 "file") with the file name
            k = Key(bucket)
            k.key = image.name
            # "Write" to S3 from the temp file
            k.set_contents_from_filename(tmp.name)
        tmp.close()
