from datetime import datetime
from typing import List
from simplistic.base import BaseBlock


class Block(BaseBlock):
    pass


class Style(Block):
    template: str = """
        html * {
            font-family: "{{ font_family }}";
            line-height: {{ line_height }};
        }
        div {
            font-size: {{ font_size }};
            width: {{ percentage }}
        }
    """
    font_size: str = "13px"
    font_family: str = """ui-sans-serif, -apple-system, BlinkMacSystemFont, Roboto, "Helvetica", "Arial", "Segoe UI", "Inter", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Microsoft YaHei Light", sans-serif"""
    line_height: float = 1.5
    percentage: str = "33%"


class Banner(Block):
    template: str = """
<a href="../../" style="text-decoration: none; color: inherit;">
<pre style="all:revert;font-size: 10px;font-family: monospace,-webkit-pictograph;line-height: 1">
{{text}}
</pre>
</a>                                                 
"""
    text: str = """
█▀▀ ─▀─ █▀▄▀█ █▀▀█ █── ─▀─ █▀▀ ▀▀█▀▀ ─▀─ █▀▀ 
▀▀█ ▀█▀ █─▀─█ █──█ █── ▀█▀ ▀▀█ ──█── ▀█▀ █── 
▀▀▀ ▀▀▀ ▀───▀ █▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀ ──▀── ▀▀▀ ▀▀▀
"""  # ASCII BANNER GENERATOR: https://fsymbols.com/generators/smallcaps/


class Breadcrumb(Block):
    template: str = """
        <p><a href="{{ href }}" style="text-decoration:none;">{{ text }}</a></p>
    """
    template: str = ""
    text: str = ".."
    href: str = "../../"


class Content(Block):
    template: str = """
        <p>{{ title }} @{{ created_at.strftime("%Y-%m-%d %H:%M:%S") }}</p>
        {{ text }}
    """
    title: str
    created_at: datetime
    text: str
    href: str


class ContentEntry(Content):
    template: str = """
        <li style="list-style-type:none;">
        @{{ created_at.strftime("%Y/%m/%d %H:%M:%S") }}  <a href="{{ href }}">{{ title }}</a>
        </li>
    """


class Footer(Block):
    template: str = """
        <footer>
            </br>&copy;<a href="{{ href }}" style="text-decoration:none; color:inherit;" >{{ text }}</a>
        </footer>
    """
    template: str = ""
    text: str
    href: str = "../../"
