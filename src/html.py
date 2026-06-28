from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

CSS = "https://cdn.simplecss.org/simple.min.css"


def generate_html(config: dict) -> None:
    """
    Generate all HTML pages.
    """

    for show in config["shows"]:
        generate_show_page(show)

    generate_index(config)


def generate_show_page(show: dict) -> None:
    """
    Generate the HTML page for a single show.
    """

    html = ET.Element("html", lang="en")

    head = ET.SubElement(html, "head")

    ET.SubElement(head, "meta", charset="utf-8")

    ET.SubElement(
        head,
        "meta",
        name="viewport",
        content="width=device-width, initial-scale=1",
    )

    ET.SubElement(head, "title").text = show["title"]

    ET.SubElement(
        head,
        "link",
        rel="stylesheet",
        href=CSS,
    )

    body = ET.SubElement(html, "body")

    ET.SubElement(body, "h1").text = show["title"]

    if show["icon"]:
        p = ET.SubElement(body, "p")

        a = ET.SubElement(
            p,
            "a",
            href=show["url"],
            target="_blank",
        )

        ET.SubElement(
            a,
            "img",
            src=show["icon"],
            alt="",
            style="max-width:256px",
        )

    if show["description"]:
        ET.SubElement(
            body,
            "p",
        ).text = show["description"]

    p = ET.SubElement(body, "p")

    ET.SubElement(
        p,
        "a",
        href=show["url"],
        target="_blank",
    ).text = "Original source"

    p = ET.SubElement(body, "p")

    ET.SubElement(
        p,
        "a",
        href="feed.xml",
        attrib={
            "class": "button",
        },
    ).text = "Subscribe"

    write_html(
        show["directory"] / "index.html",
        html,
    )


def generate_index(config: dict) -> None:
    """
    Generate the site index.
    """

    html = ET.Element("html", lang="en")

    head = ET.SubElement(html, "head")

    ET.SubElement(head, "meta", charset="utf-8")

    ET.SubElement(
        head,
        "meta",
        name="viewport",
        content="width=device-width, initial-scale=1",
    )

    ET.SubElement(
        head,
        "title",
    ).text = config["title"]

    ET.SubElement(
        head,
        "link",
        rel="stylesheet",
        href=CSS,
    )

    body = ET.SubElement(html, "body")

    ET.SubElement(
        body,
        "h1",
    ).text = config["title"]

    if config["description"]:
        ET.SubElement(
            body,
            "p",
        ).text = config["description"]

    ul = ET.SubElement(body, "ul")

    for show in config["shows"]:

        li = ET.SubElement(ul, "li")

        strong = ET.SubElement(li, "strong")

        a = ET.SubElement(
            strong,
            "a",
            href=f"/podcasts/{show['slug']}/",
        )

        a.text = show["title"]

        if show["description"]:
            ET.SubElement(li, "br")

            li.tail = None

            desc = ET.SubElement(li, "span")
            desc.text = show["description"]

    write_html(
        config["output_dir"] / "index.html",
        html,
    )


def write_html(
    filename: Path,
    root: ET.Element,
) -> None:
    """
    Write an HTML document.
    """

    tree = ET.ElementTree(root)

    ET.indent(tree, space="  ")

    with filename.open(
        "wb",
    ) as f:

        f.write(b"<!DOCTYPE html>\n")

        tree.write(
            f,
            encoding="utf-8",
            xml_declaration=False,
            short_empty_elements=True,
        )
