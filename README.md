Django HTML Emailer
===================

A utility app for sending HTML emails in Django 1.7+:

* Uses [HTML Email Boilerplate v0.5](http://htmlemailboilerplate.com/)
* Inlines CSS (per the boilerplate's instructions) using [pynliner](https://pythonhosted.org/pynliner/).
* Renders message body from Markdown or from text and HTML parts that you give.

Installation
------------

Install this module:

	pip install django-html-emailer

Add `htmlemailer` to your Django settings's INSTALLED_APPS.

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

1. A template storing the actual content of your email (either a Markdown template or a pair of templates, one for the HTML part and one for the plain text part), which extends...
2. A template that has the general design of all of your emails (CSS, header, footer), akin to your `base.html` for your site (a pair of templates, one for HTML and one for text), which extends...
3. The HTML Email Boilerplate, which we've already converted into a template.
4. A `..._subject.txt` template which generates the subject line of the email (it's also a template so you can use variables etc. in it).

First copy the example "general design" template files into your project's templates path, naming them as you like. Copy them from:

* [htmlemailer/templates/htmlemailer/example_template.txt](htmlemailer/templates/htmlemailer/example_template.txt)
* [htmlemailer/templates/htmlemailer/example_template.html](htmlemailer/templates/htmlemailer/example_template.html)

Then copy the example "actual content" template files into your project:

* [htmlemailer/templates/htmlemailer/example_subject.txt](htmlemailer/templates/htmlemailer/example_subject.txt)

and either

* [htmlemailer/templates/htmlemailer/example.md](htmlemailer/templates/htmlemailer/example.md)

if you want to use a single Markdown file or

* [htmlemailer/templates/htmlemailer/example.txt](htmlemailer/templates/htmlemailer/example.txt)
* [htmlemailer/templates/htmlemailer/example.html](htmlemailer/templates/htmlemailer/example.html)

if you want to explicitly set the text and HTML parts of the message separately.

You can change the path and file names, except the set of files must have the *same* path name up to `.md`, `.txt`, `.html`, and `_subject.txt`. That's how the module knows they go together (note how you don't include the file extension in the call to `send_mail`).

If you changed the path of the general design templates, you'll have to update the `{% extends ... %}` template tags in `example.md` or `example.txt` and `example.html` to point to the new path. You can of course have more than one email by creating a new set of `.md`, `.txt`, `.html`, and `_subject.txt` files at a different path.

Lastly, in your call to `send_mail`, update the first argument to specify the location of your email templates. Just specify the common part of the path name of the three files. In this case, it's just `htmlemailer/example`. The `.md`, `.txt`, `.html`, and `_subject.txt` will be added by the library.

Advanced Usage
--------------

`send_mail` also takes an optional `fail_silently` boolean argument (default is False), and it passes other keyword arguments on to Django's [EmailMessage](https://docs.djangoproject.com/en/1.7/topics/email/#django.core.mail.EmailMessage) constructor, so you can also pass `headers` and `connection`.

If `DEFAULT_TEMPLATE_CONTEXT` is set in your settings, then it should be a dictionary with default template context variables passed into your email templates.

Notes on Markdown
-----------------

Markdown messages are rendered into HTML using CommonMark ([specification](http://spec.commonmark.org/), [library](https://pypi.python.org/pypi/CommonMark)). The text part of the message is rendered using a special Markdown-to-text renderer, because raw Markdown doesn't always look professional (especially links and images).

The Markdown is rendered *first* prior to running the Django template engine. So you cannot cause Markdown to be inserted into the email through template context variables. This is by design.

Also note that the `{% extends ... %}` tag at the top of the Markdown message body template does not contain the `.txt` or `.html` file extension. The library inserts the right file extension for the general design template prior to rendering into HTML and text.

Note: The CommonMark library is monkey-patched to turn off escaping of {'s and }'s in URLs (to allow for template tags to appear within links). If you are using CommonMark elsewhere in your application, that might affect you if you are creating Markdown documents with these characters in URLs (which is probably bad anyway).

Testing (Library Developers)
----------------------------

A test Django project is included. To use:

	cd test_project
	pip3 install pynliner commonmark commonmarkextensions
	python3 manage.py test_html_email example
	python3 manage.py test_html_email example2

This will output test emails (a MIME message) to the console. `example` uses separate text and HTML parts. `example2` uses a single Markdown body file.

License
-------

This project and the (upstream) boilerplate code are available under the MIT license.

For Project Maintainers
-----------------------

To publish a universal wheel to pypi:

    pip3 install twine
    rm -rf dist
    python3 setup.py bdist_wheel --universal
    twine upload dist/*
    git tag v1.0.XXX
    git push --tags
