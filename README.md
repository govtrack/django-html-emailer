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

Copy the example template files:

* htmlemailer/templates/htmlemailer/example.txt
* htmlemailer/templates/htmlemailer/example.html
* htmlemailer/templates/htmlemailer/example_subject.txt

to your own location, replace the contents, update the path in the `send_mail` call, and you are good to go.

`send_mail` passes keyword arguments on to Django's `send_mail`, so you can also pass `fail_silently` (default is False), `auth_user`, `auth_password`, and `connection`.

License:

This project and the (upstream) boilerplate code are available under the MIT license.
