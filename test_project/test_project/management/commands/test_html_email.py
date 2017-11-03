from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = 'templatename [recipient@address.com [sender@address.com]]'

    def add_arguments(self, parser):
        parser.add_argument('templatename')
        parser.add_argument('recipient', nargs="?", default="recipient@example.org")
        parser.add_argument('sender', nargs="?", default="Your Site <sender@example.org>")

    def handle(self, *args, **options):
        from htmlemailer import send_mail

        send_mail(
            options["templatename"],
            options["sender"],
            [options["recipient"]],

            # example template context
            {
                "message": "This is a message containing >>> some HTML characters to test escaping <<<<.",
                "link": "https://github.com/if-then-fund/django-html-emailer",
            })
