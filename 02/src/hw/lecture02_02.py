import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Protocol

CWD: Final = Path(__file__).parent


class Model(Protocol):
    def to_element(self) -> ET.Element: ...


@dataclass
class Chapter(Model):
    id: int
    name: str
    pages: int

    def to_element(self) -> ET.Element:
        return ET.Element(
            "chapter",
            {
                "id": str(self.id),
                "name": self.name,
                "pages": str(self.pages),
            },
        )


@dataclass
class Article(Model):
    title: str
    chapters: list[Chapter]

    def to_element(self) -> ET.Element:
        elem = ET.Element("article", {"title": self.title})
        elem.extend(chapter.to_element() for chapter in self.chapters)
        return elem


@dataclass
class Novel(Model):
    chapters: list[Chapter]

    def to_element(self) -> ET.Element:
        elem = ET.Element("novel")
        elem.extend(chapter.to_element() for chapter in self.chapters)
        return elem


@dataclass
class Book(Model):
    title: str
    articles: list[Article]
    novels: list[Novel]

    def to_element(self) -> ET.Element:
        root = ET.Element("book")
        root.extend(article.to_element() for article in self.articles)
        root.extend(novel.to_element() for novel in self.novels)
        return root


BOOK: Final = Book(
    title="卒業論文",
    articles=[
        Article(
            title="卒業論文",
            chapters=[
                Chapter(id=1, name="はじめに", pages=2),
                Chapter(id=2, name="基礎理論", pages=8),
                Chapter(id=3, name="実験方法", pages=6),
                Chapter(id=4, name="結果と考察", pages=2),
                Chapter(id=5, name="まとめ", pages=1),
                Chapter(id=6, name="参考文献", pages=2),
            ],
        ),
    ],
    novels=[
        Novel(
            chapters=[
                Chapter(id=1, name="1日のはじまり", pages=2),
                Chapter(id=2, name="朝食", pages=8),
                Chapter(id=3, name="仕事", pages=6),
                Chapter(id=4, name="帰宅後", pages=2),
                Chapter(id=5, name="新しい朝", pages=1),
            ],
        ),
    ],
)


def lecture02_02() -> None:
    book_elem = BOOK.to_element()
    ET.indent(book_elem, space="  ")
    tree = ET.ElementTree(book_elem)
    tree.write(CWD / "lecture02_02_data.xml", encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    lecture02_02()
