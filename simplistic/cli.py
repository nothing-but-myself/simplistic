import contextlib
from functools import partial
import os
import shutil
import socket
import click
from simplistic.page import Post, Index
from simplistic.block import Content, ContentEntry
from http.server import ThreadingHTTPServer, test, SimpleHTTPRequestHandler
from markdown import markdown


ALL_EXTENSIONS = [
    "extra",
    "abbr",
    "attr_list",
    "def_list",
    "fenced_code",
    "footnotes",
    "md_in_html",
    "tables",
    "admonition",
    "codehilite",
    "legacy_attrs",
    "legacy_em",
    "meta",
    "nl2br",
    "sane_lists",
    "smarty",
    "toc",
    "wikilinks",
]

# ALL_EXTENSIONS = [
#     "pymdownx.betterem",
#     "pymdownx.superfences",
#     "markdown.extensions.footnotes",
#     "markdown.extensions.attr_list",
#     "markdown.extensions.def_list",
#     "markdown.extensions.tables",
#     "markdown.extensions.abbr",
#     "markdown.extensions.md_in_html",
# ]


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--src",
    default=os.path.join(os.getcwd(), "contents"),
    type=str,
    show_default=True,
)
@click.option(
    "--dst",
    default=os.path.join(os.getcwd(), "docs"),
    type=str,
    show_default=True,
)
def gen(src: str, dst: str):
    name_to_ctime = {
        filename: os.stat(os.path.join(src, filename)).st_ctime
        for filename in os.listdir(src)
    }
    index = Index(dst=dst, content=[], posts=[])
    for idx, (filename, ctime) in enumerate(
        sorted(name_to_ctime.items(), key=lambda x: x[-1]),
        start=1,
    ):
        path = os.path.join(os.path.join(src, filename))
        title, _ = os.path.splitext(filename)
        with open(path) as f:
            content = Content(
                text=markdown(f.read(), extensions=ALL_EXTENSIONS),
                title=title,
                created_at=ctime,
                href="./p/{}/".format(idx),
            )
        content_entry = ContentEntry(**content.model_dump(exclude={"template"}))
        post = Post(dst=os.path.join(dst, "p/{}".format(idx)), content=content)
        index.content.append(content_entry)
        index.posts.append(post)

    return index.generate()


@cli.command()
@click.option("--port", default=8000, type=int, show_default=True)
@click.option(
    "--directory",
    default=os.path.join(os.getcwd(), "docs"),
    type=str,
    show_default=True,
)
def run(port: int, directory: str):
    directory = os.path.join(os.getcwd(), directory)

    class DualStackServer(ThreadingHTTPServer):
        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

    return test(
        HandlerClass=partial(SimpleHTTPRequestHandler, directory=directory),
        ServerClass=DualStackServer,
        port=port,
    )


@cli.command()
@click.option(
    "--directory",
    default=os.path.join(os.getcwd(), "docs"),
    type=str,
    show_default=True,
)
def clean(directory: str):
    directory = os.path.join(os.getcwd(), directory)
    return shutil.rmtree(directory)
