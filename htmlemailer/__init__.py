from django.template.exceptions import TemplateDoesNotExist
from django.template.base import Template, Context
from django.template.engine import Engine
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

import re

import pynliner
import CommonMark
import CommonMarkExtensions.plaintext

def send_mail(template_prefix, from_email, recipient_list, template_context, fail_silently=False, **kwargs):
    # Sends a templated HTML email.
    #
    # Unrecognized arguments are passed on to Django's EmailMultiAlternatives's init method.

    # add default template context variables from settings.DEFAULT_TEMPLATE_CONTEXT
    template_context = build_template_context(template_context)

    # subject
    subject = render_to_string(template_prefix + '_subject.txt', template_context)
    subject = re.sub(r"\s*[\n\r]+\s*", " ", subject).strip()  # remove superfluous internal white space around line breaks and leading/trailing spaces

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


def render_from_markdown(template, template_context):
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
    # Do this within each {% block %}...{% endblock %} tag, since we
    # don't want to create HTML <p>s around content that doesn't occur
    # within a block. Assumes there are no nested blocks.
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

    # Build the HTML and text templates.

    def run_renderer(renderer, ext, wrap=lambda x : x):
        r = template

        # fix the {% extends "..." %} file extension.
        r = re.sub(
            r"^(\s*\{%\s*extends\s+\"[^\"]*)(\"\s*%\})",
            lambda m : m.group(1) + "." + ext + m.group(2),
            r)

        # Run CommonMark on each block separately.
        r = re.sub(
            r"(\{%\s*block [^%]+\s*%\})\s*([\s\S]*?)\s*(\{%\s*endblock\s*%\})",
            lambda m : m.group(1)
                     + wrap(renderer.render(CommonMark.Parser().parse(m.group(2))))
                     + m.group(3),
            r
            )

        return r

    # Render to HTML, put the extends tag back with an .html extension.
    html_body = run_renderer(CommonMark.HtmlRenderer({ "safe": False }), 'html')

    # For the text portion, we'll render using a special renderer, and we'll
    # wrap each block in the Django template directive to turn off auto-escaping.
    text_body = run_renderer(CommonMarkExtensions.plaintext.PlainTextRenderer(), 'txt',
        wrap = lambda block : "{% autoescape off %}" + block + "{% endautoescape %}")

    # Now render as Django templates.
    html_body = Template(html_body).render(Context(template_context)).strip()
    text_body = Template(text_body).render(Context(template_context)).strip()
    return text_body, html_body
