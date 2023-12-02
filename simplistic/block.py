from datetime import datetime
from typing import List
from simplistic.base import BaseBlock


class Block(BaseBlock):
    pass


class Style(Block):
    template: str = """
        @font-face {
            font-family: TwitterChirp;
            src: url(https://abs.twimg.com/responsive-web/client-web/Chirp-Light.3a18e64a.woff2) format('woff2'), url(https://abs.twimg.com/responsive-web/client-web/Chirp-Light.7a5673aa.woff) format('woff');
            font-weight: 300;
            font-style: 'normal';
            font-display: 'swap';
        }
        html * {
            font-family: "TwitterChirp";
            font-size: {{ font_size }}px;
            line-height: {{ line_height }};
        }
        div {
            width: {{ percentage }}
        }
    """
    font_size: int = 15
    font_family: str = "STFangsong"
    line_height: float = 1.33
    percentage: str = "33%"


class Banner(Block):
    template: str = """
        <div font-size="40" line-height="1.5">
            {{ text }}
        </div>                                                   
    """
    text: str = "HEY,"

class Breadcrumb(Block):
    template: str = """
        <a href="{{ href }}">{{ text }}</a>
    """
    # template: str = ""
    text: str = ".."
    href: str = "/"


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


class TableOfContent(Block):
    template: str = """
        <div>
        {% for content in contents %}
            <li style="list-style-type:none;">
            @{{ content.created_at.strftime("%Y/%m/%d %H:%M:%S") }}  <a href="{{ content.href }}">{{ content.title }}</a>
            </li>
        {% endfor %}
        </div>
    """
    contents: List[Content]


class Footer(Block):
    template: str = """
        <footer>
            </br>&copy;<a href="{{ href }}" style="text-decoration:none; color:inherit;" >{{ text }}</a>
        </footer>
    """
    text: str
    href: str = "/"
