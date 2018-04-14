from django.core.management.base import NoArgsCommand

from crimsononline.content.models import Content


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = 'Sets the right content type on Content objects'

    def handle_noargs(self, **options):
        models = [t.model_class() for t in Content.types()]
        for m in models:
            for o in m.objects.all_objects():
                o.content_type = None
                o.save()
