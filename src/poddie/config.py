from __future__ import annotations

import hashlib
import os
import re
import unicodedata
from pathlib import Path

import yaml


DEFAULT_CONFIG = "/config/config.yml"
DEFAULT_OUTPUT = "/data"


def slugify(title: str) -> str:
    """
    Generate a human-readable slug from a show's title.
    """

    text = unicodedata.normalize("NFKD", title)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = text.replace("&", " and ")
    text = text.replace("'", "")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")

    return text or "podcast"


def slug_hash(url: str) -> str:
    """
    Generate a short deterministic hash from a show's URL.
    """

    return hashlib.sha1(
        url.encode("utf-8"),
        usedforsecurity=False,
    ).hexdigest()[:8]


def load_config() -> dict:
    """
    Load the Poddie configuration.

    Configuration file location can be overridden with:

        PODDIE_CONFIG=/path/to/config.yml

    Output directory can be overridden with:

        PODDIE_OUTPUT=/data
    """

    config_file = Path(
        os.environ.get(
            "PODDIE_CONFIG",
            DEFAULT_CONFIG,
        )
    )

    output_dir = Path(
        os.environ.get(
            "PODDIE_OUTPUT",
            DEFAULT_OUTPUT,
        )
    )

    with config_file.open(
        "r",
        encoding="utf-8",
    ) as f:
        config = yaml.safe_load(f)

    if config is None:
        config = {}

    config.setdefault("title", "Podcasts")
    config.setdefault("description", "")
    config.setdefault("base_url", "http://localhost")
    config.setdefault("update_interval", 43200)
    config.setdefault("shows", [])

    config["output_dir"] = output_dir

    used_slugs: set[str] = set()

    # Populate derived values for each show.
    for show in config["shows"]:
        show.setdefault("description", "")
        show.setdefault("icon", "")
        show.setdefault("max_episodes", 10)

        base_slug = slugify(show["title"])

        slug = base_slug

        if slug in used_slugs:
            slug = f"{base_slug}-{slug_hash(show['url'])}"

            while slug in used_slugs:
                slug = f"{base_slug}-{slug_hash(slug)}"

        used_slugs.add(slug)

        show["slug"] = slug

        show["directory"] = (
            output_dir
            / "podcasts"
            / slug
        )

        show["directory"].mkdir(
            parents=True,
            exist_ok=True,
        )

    # Create the podcasts directory used by the HTML index.
    (
        output_dir / "podcasts"
    ).mkdir(
        parents=True,
        exist_ok=True,
    )

    return config
