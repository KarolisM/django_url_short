from optparse import make_option
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
from django_url_short.settings import LINK_EXPIRATION_DELTA
from django_url_short.models import LinkDestination

prompt_msg = _(u'Do you want to delete {obj}?')


class Command(BaseCommand):
    model = LinkDestination

    help = 'Deletes links that have already expired.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interactive',
            action='store_true',
            dest='interactive',
            default=False,
            help='Prompt confirmation before each deletion.'
        )

    def handle(self, *args, **options):
        interactive = options.get('interactive')
        q = self.model.objects.all()

        ct = 0
        for e in q:
            if e.expired:
                if interactive:
                    prompt = prompt_msg.format(obj=e) + u' (y/n): '
                    answer = input(prompt).lower()
                    while answer not in ('y', 'n'):
                        answer = input(prompt).lower()
                    if answer == 'n':
                        continue
                e.delete()
                ct += 1

        print(f'Number of links removed: {ct}')