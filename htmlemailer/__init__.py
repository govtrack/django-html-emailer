from django.template.exceptions import TemplateDoesNotExist
from django.template.base import Template, Context
from django.template.engine import Engine
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

import re

import pynliner
import CommonMark
import CommonMarkPlainText

def send_mail(template_prefix, from_email, recipient_list, template_context, fail_silently=False, **kwargs):
    # Sends a templated HTML email.
    #
    # Unrecognized arguments are passed on to Django's EmailMultiAlternatives's init method.

    # add default template context variables from settings.DEFAULT_TEMPLATE_CONTEXT
    template_context = build_template_context(template_context)

    # subject
    subject = render_to_string(template_prefix + '_subject.txt', template_context)
    subject = ''.join(subject.splitlines()).strip()  # remove superfluous line breaks and trailing spaces

    # Add subject as a new context variable, and it is used in the base HTML template's title tag.
    template_context['subject'] = subject

    # body

    # see if a Markdown template is present
    try:
        # Use the template engine's loaders to find the template, but then just
        # ask for its source so we have the raw Markdown.
        md_template = Engine.get_default().get_template(template_prefix + '.md').source
    except TemplateDoesNotExist:
        md_template = None

    if md_template:
        # render the text and HTML parts from the Markdown template
        text_body, html_body = render_from_markdown(md_template, template_context)
    else:
        # render from separate text and html templates
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


def render_from_markdown(md, template_context):
    # Strip the "extends" tag.
    m = re.match(r"\s*\{\%\s+extends\s+\"([^\"]*)\" \%\}", md)
    extends_template = None
    if m:
        extends_template = m.group(1)
        m = m.group(0)
        md = md[len(m):]

    # Render the Markdown first. Markdown has different text escaping rules
    # (backslash-escaping of certain symbols only), and we can't add that
    # logic to Django's template auto-escaping. So we render the Markdown
    # first, which gives HTML. That HTML can be treated as a regular Django
    # template (with regular HTML autoescaping).
    #
    # (If we did it in the other order, we'd have to disable Django's
    # HTML autoescaping and then have some other method to prevent the
    # use of variables in the template from generating Markdown tags.)
    #
    # We turn off CommonMark's safe mode, however, since we trust the
    # template. (Safe mode prohibits HTML inlines and also prevents some
    # unsafe URLs, but that's up to the caller.)

    # CommonMark replaces non-URL-safe characters in link URLs with
    # their %-escaped code. Monkey-patch the CommonMark library to
    # not do that for { and } so that template variables within links
    # remain a template variable and don't turn into %7B%7Bvarname%7D%7D.
    # Do this prior to parsing.
    from CommonMark import common, inlines
    def fixed_normalize_uri(uri):
        return common.normalize_uri(uri).replace("%7B", "{").replace("%7D", "}")
    inlines.normalize_uri = fixed_normalize_uri

    # Parse the Markdown.
    md = CommonMark.Parser().parse(md)

    # Render to HTML, put the extends tag back with an .html extension.
    html_body = CommonMark.HtmlRenderer({ "safe": False }).render(md)
    if extends_template:
        html_body = "{% extends \"" + extends_template + ".html" + "\" %}\n" + html_body

    # For the text portion, we'll render using a special renderer (see
    # below), then wrap in a Django tag to turn off autoescaping, and
    # then put back the extends tag but with a .txt extension.
    text_body = CommonMarkPlainText.CommonMarkPlainTextRenderer().render(md)
    text_body = "{% autoescape off %}" + text_body + "{% endautoescape %}"
    if extends_template:
        text_body = "{% extends \"" + extends_template + ".txt" + "\" %}\n" + text_body

    # Now render as Django templates.
    html_body = Template(html_body).render(Context(template_context)).strip()
    text_body = Template(text_body).render(Context(template_context)).strip()
    return text_body, html_body
