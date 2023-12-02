import contextlib
from functools import partial
import os
import shutil
import socket
import click
from simplistic.page import Post, Index
from simplistic.block import Content, TableOfContent
from http.server import ThreadingHTTPServer, test, SimpleHTTPRequestHandler


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
    contents = list()
    for index, (filename, ctime) in enumerate(
        sorted(name_to_ctime.items(), key=lambda x: x[-1]),
        start=1,
    ):
        path = os.path.join(os.path.join(src, filename))
        title, _ = os.path.splitext(filename)
        with open(path) as f:
            content = Content(
                text=f.read(), title=title, created_at=ctime, href="p/{}/".format(index)
            )
            contents.append(content)
            _ = Post(
                dst=os.path.join(dst, "p/{}".format(index)),
                content=content,
            ).generate()

    return Index(
        dst=dst,
        content=TableOfContent(contents=contents),
    ).generate()


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
