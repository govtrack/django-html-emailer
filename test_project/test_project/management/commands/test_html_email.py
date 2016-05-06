from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = 'templatename [recipient@address.com [sender@address.com]]'

    def handle(self, *args, **options):
        if len(args) == 0:
            print("Specify the base name of a template.")
            return

        template, recipient_address, sender_address = \
            args + tuple(reversed(["recipient@example.org", "Your Site <sender@example.org>"]))

        from htmlemailer import send_mail

        send_mail(
            template,
            sender_address,
            [recipient_address],

            # example template context
            {
                "message": "This is a message containing >>> some HTML characters to test escaping <<<<."
            })
