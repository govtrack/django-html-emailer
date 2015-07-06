Django HTML Emailer
===================

A utility app for sending HTML emails in Django 1.7+:

* Uses [HTML Email Boilerplate v0.5](http://htmlemailboilerplate.com/)
* Inlines CSS (per the boilerplate's instructions) using [pynliner](https://pythonhosted.org/pynliner/).

Usage:

For Python 3, first run:

    pip install git+https://github.com/dcramer/pynliner@python3

before proceeding to get a Python 3-compatible version of pyliner.

Install this module:

	# pip install django-html-emailer # not working yet...
	
	pip install git+https://this-repository-url

Add `htmlemailer` to your INSTALLED_APPS.

Test if things are OK so far. Run this:

	from htmlemailer import send_mail

	send_mail(
		"htmlemailer/example",
		"My Site <mysite@example.org>",
		["you@recipient.com"],
		{
			"my_message": "Hello & good day to you!"
		})

Replace the recipient address with your email address. This should send you a message using the example template.

Copy the example base template files into your project (and name them as you like). These files provide a place to set default styling, footer text, etc. that apply across all of your emails, like base.html does for your web templates.

* htmlemailer/templates/htmlemailer/example_template.txt
* htmlemailer/templates/htmlemailer/example_template.html

Copy the example email files into your project (and name them as you like) to provide the content for particular emails.

* htmlemailer/templates/htmlemailer/example.txt
* htmlemailer/templates/htmlemailer/example.html
* htmlemailer/templates/htmlemailer/example_subject.txt

The email templates (example.txt, exmaple.html) specify the path to the base templates (example_template.txt, example_template.html), so you'll need to update the paths there to where you put your base templates. Then update the path in the `send_mail` call to specify the location of your email templates.

`send_mail` also takes an optional `fail_silently` boolean argument (default is False), and it passes other keyword arguments on to Django's [EmailMessage](https://docs.djangoproject.com/en/1.7/topics/email/#django.core.mail.EmailMessage) constructor, so you can also pass `headers` and `connection`.

License:

This project and the (upstream) boilerplate code are available under the MIT license.
