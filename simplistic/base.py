import os
import jinja2
from typing import Any, Dict
from pydantic import BaseModel
from abc import ABC, abstractmethod


class Template(ABC, BaseModel):
    template: str

    @abstractmethod
    def data(self) -> Dict[str, Any]:
        pass


class Renderer(ABC):
    @abstractmethod
    def render(self):
        pass


class Generator(ABC):
    @abstractmethod
    def generate(self):
        pass


class BaseBlock(Template, Renderer):
    def data(self) -> Dict[str, Any]:
        return {
            key: val.render() if isinstance(val, BaseBlock) else val
            for key, val in self
            if key not in ["template"]
        }

    def render(self):
        tpl = jinja2.Template(self.template)
        return tpl.render(
            **self.data(),
        )


class BasePage(Template, Generator):
    name: str = "index"
    ext: str = "html"
    dst: str = "docs"

    def data(self) -> Dict[str, Any]:
        return {
            key: val.render() if isinstance(val, BaseBlock) else val
            for key, val in self
            if key not in ["template", "name", "ext", "dst"]
        }

    def generate(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        filename = f"{self.name}.{self.ext}"
        tpl = jinja2.Template(self.template)
        dst = os.path.join(dirname, self.dst, filename)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        return tpl.stream(
            **self.data(),
        ).dump(dst)
