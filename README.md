Django HTML Emailer
===================

A utility app for sending HTML emails in Django 1.7+:

* Uses [HTML Email Boilerplate v0.5](http://htmlemailboilerplate.com/)
* Inlines CSS (per the boilerplate's instructions) using [pynliner](https://pythonhosted.org/pynliner/).

Installation
------------

Install this module: (sorry it's not on pypi yet)

	pip install git+https://github.com/if-then-fund/django-html-emailer

Add `htmlemailer` to your INSTALLED_APPS.

Basic Usage
-----------

Here's a quick example for how to send a message:

	from htmlemailer import send_mail

	send_mail(
		"htmlemailer/example",
		"My Site <mysite@example.org>",
		["you@recipient.com"],
		{
			"my_message": "Hello & good day to you!"
		})

Replace the recipient address with your email address. This should send you a message using the example template.

Your Templates
--------------

htmlemailer composes your actual email from a series of templates. Usually you have:

1. A template storing the actual content of your email (actually a pair of templates, one for the HTML part and one for the plain text part), which extends...
2. A template that has the general design of all of your emails (CSS, header, footer), akin to your `base.html` for your site (again actually a pair, one for HTML and one for text), which extends...
3. The HTML Email Boilerplate, which we've already converted into a template.
4. A `..._subject.txt` template which generates the subject line of the email (it's also a template so you can use variables etc. in it).

First copy the example "general design" template files into your project, naming them as you like. Copy them from:

* htmlemailer/templates/htmlemailer/example_template.txt
* htmlemailer/templates/htmlemailer/example_template.html

Then copy the example "actual content" template files into your project. You can change the path and file names, except the three files must have the *same* path name up to `.txt`, `.html`, and `_subject.txt`. That's how the module knows they go together. Our examples for you to copy are stored in:

* htmlemailer/templates/htmlemailer/example.txt
* htmlemailer/templates/htmlemailer/example.html
* htmlemailer/templates/htmlemailer/example_subject.txt

If you changed the path of the general design templates, you'll have to update the `{% extends ... %}` template tags in `example.txt` and `example.html` to point to the new path. You can of course have more than one email by creating a new set of `.txt`, `.html`, and `_subject.txt` files at a different path.

Lastly, in your call to `send_mail`, update the first argument to specify the location of your email templates. Just specify the common part of the path name of the three files. In this case, it's just `htmlemailer/example`. The `.txt`, `.html`, and `_subject.txt` will be added by the library.

Advanced Usage
--------------

`send_mail` also takes an optional `fail_silently` boolean argument (default is False), and it passes other keyword arguments on to Django's [EmailMessage](https://docs.djangoproject.com/en/1.7/topics/email/#django.core.mail.EmailMessage) constructor, so you can also pass `headers` and `connection`.

If `DEFAULT_TEMPLATE_CONTEXT` is set in your settings, then it should be a dictionary with default template context variables passed into your email templates.

License
-------

This project and the (upstream) boilerplate code are available under the MIT license.
