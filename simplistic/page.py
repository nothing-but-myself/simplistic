import os
from simplistic.base import BasePage
from simplistic.block import Style, Banner, Content, Footer, Breadcrumb, TableOfContent


class Page(BasePage):
    template: str = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
            <style>{% block style %}{{ style }}{% endblock %}</style>
        </head>
        <body>
            {% block banner %}
                {{ banner }}
            {% endblock %}

            {% block breadcrumb %}
                {{ breadcrumb }}
            {% endblock %}

            {% block content %}
                {{ content }}
            {% endblock %}

            {% block footer %}
                {{ footer }}
            {% endblock %}
        </body>
        </html>
    """
    title: str = "SIMPLISTIC"
    style: Style = Style()
    banner: Banner = Banner()
    breadcrumb: Breadcrumb = Breadcrumb()
    footer: Footer = Footer(text="SIMPLISTIC")


class Post(Page):
    dst: str
    content: Content


class Index(Page):
    dst: str = "docs/"
    content: TableOfContent
