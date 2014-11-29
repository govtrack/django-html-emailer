from django.template.loader import render_to_string

from django.core.mail import send_mail as django_send_mail

import pynliner

def send_mail(template_prefix, from_email, recipient_list, template_context, **kwargs):
	# Sends a templated HTML email.
	#
	# Unrecognized arguments are passed on to Django's send_mail, so
	# you may also want to pass:
	#   fail_silently (default is False)
	#   auth_user, auth_password, connection
	# But do not pass html_message, since that is sent by us.

	if not template_context:
		# initialize if empty
		template_context = { }
	else:
		# clone
		template_context = dict(template_context)

	# subject
	subject = render_to_string(template_prefix + '_subject.txt', template_context)
	subject = ''.join(subject.splitlines())  # remove superfluous line breaks
	template_context['subject'] = subject

	# body
	text_body = render_to_string(template_prefix + '.txt', template_context)
	html_body = render_to_string(template_prefix + '.html', template_context)

	# inline HTML styles because some mail clients dont process the <style> tag
	html_body = pynliner.fromString(html_body)

	# send!
	django_send_mail(subject, text_body, from_email, recipient_list, html_message=html_body, **kwargs)
