from datetime import datetime
from typing import List
from simplistic.base import BaseBlock


class Block(BaseBlock):
    pass


class Style(Block):
    template: str = """
        html * {
            font-size: {{ font_size }}px;
            line-height: {{ line_height }};
            font-family: {{ font_family }};
        }
        div {
            width: {{ percentage }}
        }
    """
    font_size: int = 14
    # font_family: str = "STFangsong"
    line_height: float = 1.33
    percentage: str = "33%"


class Banner(Block):
    template: str = """
<pre>
 _     __    _     _         ____   __    __    ____ 
| | | / /`_ | |   \ \_/     | |_   / /\  / /`  | |_  
\_\_/ \_\_/ |_|__  |_|      |_|   /_/--\ \_\_, |_|__ 
</pre>                                                     
"""


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
            </br>@<a href="{{ href }}">{{ text }}</a>.
        </footer>
    """
    text: str
    href: str = "/"
