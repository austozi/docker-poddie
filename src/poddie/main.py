from __future__ import annotations

import logging
import signal
import time

from .config import load_config
from .downloader import download
from .html import generate_html
from .rss import generate_rss

running = True


def shutdown(signum, frame):
    global running
    running = False


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logging.info("Poddie starting")

    while running:

        config = load_config()

        for show in config["shows"]:

            logging.info(
                "Processing %s",
                show["title"],
            )

            download(show)

            generate_rss(
                show,
                config,
            )

        generate_html(config)

        if not running:
            break

        logging.info(
            "Sleeping for %d seconds",
            config["update_interval"],
        )

        time.sleep(
            config["update_interval"],
        )

    logging.info("Stopping")


if __name__ == "__main__":
    main()
