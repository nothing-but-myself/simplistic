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
    @staticmethod
    def _recur_render(elem):
        if isinstance(elem, BaseBlock):
            return elem.render()
        elif isinstance(elem, list):
            elems = [BaseBlock._recur_render(e) for e in elem]
            result = ""
            for elem in elems:
                if not isinstance(elem, str):
                    raise TypeError
                result += elem
            return result
        elif isinstance(elem, dict):
            return {k: BaseBlock._recur_render(v) for k, v in elem.items()}
        return elem

    def data(self) -> Dict[str, Any]:
        return {
            key: self._recur_render(val)
            for key, val in self
            if key
            not in [
                "template",
            ]
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

    @staticmethod
    def _recur_generate(elem):
        if isinstance(elem, BaseBlock):
            return elem.render()
        elif isinstance(elem, BasePage):
            result = elem.generate()
            if result is None:
                return ""
            return result
        elif isinstance(elem, list):
            return "".join([BasePage._recur_generate(e) for e in elem])
        elif isinstance(elem, dict):
            return {k: BasePage._recur_generate(v) for k, v in elem.items()}
        return elem

    def data(self) -> Dict[str, Any]:
        return {
            key: self._recur_generate(val)
            for key, val in self
            if key
            not in [
                "template",
                "name",
                "ext",
                "dst",
            ]
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
