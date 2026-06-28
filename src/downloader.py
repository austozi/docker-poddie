from __future__ import annotations

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def download(show: dict) -> bool:
    """
    Download new episodes for a show.

    Returns True if new MP3 files were downloaded.
    """

    directory: Path = show["directory"]

    before = {
        p.name
        for p in sorted(directory.glob("*.mp3"))
    }

    cmd = [
        "yt-dlp",
        "-f",
        "bestaudio/best",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "0",
        "--write-info-json",
        "--download-archive",
        str(directory / ".archive"),
        "--output",
        str(directory / "%(title)s.%(ext)s"),
        "--max-downloads",
        str(show["max_episodes"]),
        "--no-progress",
        show["url"],
    ]

    logger.info("Downloading %s", show["title"])
    logger.info("Running command: %s", " ".join(cmd))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    #
    # yt-dlp exits with status 101 when it reaches --max-downloads.
    # For Poddie this is expected and should not be treated as an error.
    #
    if result.returncode not in (0, 101):

        logger.error(
            "yt-dlp exited with code %d",
            result.returncode,
        )

        if result.stdout:
            logger.error(
                "yt-dlp stdout:\n%s",
                result.stdout.rstrip(),
            )

        if result.stderr:
            logger.error(
                "yt-dlp stderr:\n%s",
                result.stderr.rstrip(),
            )

        return False

    after = {
        p.name
        for p in sorted(directory.glob("*.mp3"))
    }

    new_files = after - before

    if new_files:
        logger.info(
            "Downloaded %d new episode(s).",
            len(new_files),
        )
    else:
        logger.info("No new episodes.")

    return bool(new_files)
