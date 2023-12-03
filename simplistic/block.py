from datetime import datetime
from typing import List
from simplistic.base import BaseBlock


class Block(BaseBlock):
    pass


class Style(Block):
    template: str = """
        html * {
            font-family: "{{ font_family }}";
            font-size: {{ font_size }}px;
            line-height: {{ line_height }};
        }
        div {
            width: {{ percentage }}
        }
    """
    font_size: int = 14
    font_family: str = "-apple-system,BlinkMacSystemFont,Helvetica Neue,PingFang SC,Microsoft YaHei,Source Han Sans SC,Noto Sans CJK SC,WenQuanYi Micro Hei,sans-serif"
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
    # template: str = """
    #     <p><a href="{{ href }}" style="text-decoration:none;">{{ text }}</a></p>
    # """
    template: str = ""
    text: str = ".."
    href: str = "../../"


class Content(Block):
    template: str = """
        <div>
        <p>{{ title }} @{{ created_at.strftime("%Y-%m-%d %H:%M:%S") }}</p>
        {{ text }}
        </div>
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
    # template: str = """
    #     <footer>
    #         </br>&copy;<a href="{{ href }}" style="text-decoration:none; color:inherit;" >{{ text }}</a>
    #     </footer>
    # """
    template: str = ""
    text: str
    href: str = "../../"
