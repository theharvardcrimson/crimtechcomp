import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator

from django_downloadview import StorageDownloadView, StorageFile


class ServeDocsView(StorageDownloadView):
    attachment = False
    storage = FileSystemStorage(location=settings.DOCS_ROOT)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ServeDocsView, self).dispatch(*args, **kwargs)

    def get_file(self):
        path = self.get_path()
        if os.path.isdir(self.storage.path(path)):
            path = os.path.join(path, 'index.html')
        return StorageFile(self.storage, path)
