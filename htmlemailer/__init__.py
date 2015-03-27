from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives

import pynliner

def send_mail(template_prefix, from_email, recipient_list, template_context, fail_silently=False, **kwargs):
	# Sends a templated HTML email.
	#
	# Unrecognized arguments are passed on to Django's EmailMultiAlternatives's init method.

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

	# construct MIME message
	msg = EmailMultiAlternatives(
		subject=subject,
		body=text_body,
		from_email=from_email,
		to=recipient_list,
		**kwargs
		)
	msg.attach_alternative(html_body, "text/html")

	# send!
	msg.send(fail_silently=fail_silently)
