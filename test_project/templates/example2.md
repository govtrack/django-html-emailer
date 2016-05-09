{% extends "template" %}
{% block content %}
# Hello!

* Remember.

* To use bullets.

## The message

> {{message}}

See [the project]({{link}}) for more information.

Or just a plain link: [{{link}}]({{link}})

{% endblock %}