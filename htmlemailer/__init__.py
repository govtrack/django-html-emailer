from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

import pynliner

def send_mail(template_prefix, from_email, recipient_list, template_context, fail_silently=False, **kwargs):
	# Sends a templated HTML email.
	#
	# Unrecognized arguments are passed on to Django's EmailMultiAlternatives's init method.

	# add default template context variables from settings.DEFAULT_TEMPLATE_CONTEXT
	template_context = build_template_context(template_context)

	# subject
	subject = render_to_string(template_prefix + '_subject.txt', template_context)
	subject = ''.join(subject.splitlines())  # remove superfluous line breaks

	# Add subject as a new context variable, and it is used in the base HTML template's title tag.
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


def build_template_context(user_variables):
	template_context = { }

	# Add in default context variables from the settings module, if such a setting exists.
	try:
		template_context.update(settings.DEFAULT_TEMPLATE_CONTEXT)
	except AttributeError:
		pass

	# Add in the user-provided context variables.
	if user_variables:
		template_context.update(user_variables)

	return template_context
