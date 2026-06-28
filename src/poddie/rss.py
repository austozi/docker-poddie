from __future__ import annotations

import json
import mimetypes
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

from mutagen.mp3 import MP3

ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"
ATOM_NS = "http://www.w3.org/2005/Atom"

ET.register_namespace("itunes", ITUNES_NS)
ET.register_namespace("atom", ATOM_NS)


def generate_rss(show: dict, config: dict) -> None:
    """
    Generate feed.xml for a single show.
    """

    directory: Path = show["directory"]

    episodes = []

    for info_file in sorted(directory.glob("*.info.json")):

        with info_file.open("r", encoding="utf-8") as f:
            info = json.load(f)

        mp3 = directory / (info_file.stem.replace(".info", "") + ".mp3")

        if not mp3.exists():
            continue

        episodes.append(
            {
                "info": info,
                "mp3": mp3,
            }
        )

    episodes.sort(
        key=lambda e: e["info"].get("upload_date", ""),
        reverse=True,
    )

    rss = ET.Element(
        "rss",
        {
            "version": "2.0",
        },
    )

    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = show["title"]
    ET.SubElement(channel, "link").text = show["url"]
    ET.SubElement(channel, "description").text = show["description"]
    ET.SubElement(channel, "language").text = "en-GB"

    ET.SubElement(
        channel,
        "lastBuildDate",
    ).text = format_datetime(
        datetime.now(timezone.utc)
    )

    ET.SubElement(
        channel,
        f"{{{ITUNES_NS}}}summary",
    ).text = show["description"]

    ET.SubElement(
        channel,
        f"{{{ITUNES_NS}}}image",
        {
            "href": show["icon"],
        },
    )

    ET.SubElement(
        channel,
        f"{{{ATOM_NS}}}link",
        {
            "href": (
                f'{config["base_url"]}/podcasts/'
                f'{show["slug"]}/feed.xml'
            ),
            "rel": "self",
            "type": "application/rss+xml",
        },
    )

    ET.SubElement(
        channel,
        f"{{{ITUNES_NS}}}new-feed-url",
    ).text = (
        f'{config["base_url"]}/podcasts/'
        f'{show["slug"]}/feed.xml'
    )

    image = ET.SubElement(channel, "image")
    ET.SubElement(image, "url").text = show["icon"]
    ET.SubElement(image, "title").text = show["title"]
    ET.SubElement(image, "link").text = show["url"]

    for episode in episodes:

        info = episode["info"]
        mp3 = episode["mp3"]

        item = ET.SubElement(channel, "item")

        ET.SubElement(
            item,
            "title",
        ).text = info.get(
            "title",
            mp3.stem,
        )

        ET.SubElement(
            item,
            "description",
        ).text = (
            info.get("description")
            or ""
        )

        guid = ET.SubElement(
            item,
            "guid",
            {
                "isPermaLink": "false",
            },
        )

        guid.text = (
            info.get("id")
            or mp3.name
        )

        ET.SubElement(
            item,
            "link",
        ).text = info.get(
            "webpage_url",
            show["url"],
        )

        upload_date = info.get("upload_date")

        if upload_date:
            published = datetime.strptime(
                upload_date,
                "%Y%m%d",
            ).replace(
                tzinfo=timezone.utc,
            )
        else:
            published = datetime.fromtimestamp(
                mp3.stat().st_mtime,
                tz=timezone.utc,
            )

        ET.SubElement(
            item,
            "pubDate",
        ).text = format_datetime(
            published
        )
        
        audio = MP3(mp3)

        mime = (
            mimetypes.guess_type(mp3.name)[0]
            or "audio/mpeg"
        )

        ET.SubElement(
            item,
            "enclosure",
            {
                "url": (
                    f'{config["base_url"]}/podcasts/'
                    f'{show["slug"]}/{mp3.name}'
                ),
                "length": str(
                    mp3.stat().st_size
                ),
                "type": mime,
            },
        )

        ET.SubElement(
            item,
            f"{{{ITUNES_NS}}}duration",
        ).text = str(
            int(audio.info.length)
        )

    tree = ET.ElementTree(rss)

    ET.indent(
        tree,
        space="  ",
    )

    tree.write(
        directory / "feed.xml",
        encoding="utf-8",
        xml_declaration=True,
    )
