# Poddie

Poddie is a self-hosted podcast feed generator for media available on websites supported by yt-dlp.

Poddie periodically checks configured shows for new episodes, downloads them as MP3 files, generates standard RSS podcast feeds, generates simple HTML pages, and serves everything over HTTP. You can then subscribe to the generated feeds using any podcast player.

Unlike the [original shell-script implementation](https://github.com/austozi/poddie), the current version is a single Python application with no external feed-generation dependencies.

## Features

* Downloads audio from any website supported by yt-dlp.
* Automatically updates yt-dlp on every container startup.
* Supports multiple shows.
* Generates a standard RSS podcast feed for each show.
* Generates a simple HTML page for each show.
* Generates an index page listing all configured shows.
* Downloads only new episodes using yt-dlp's download archive.
* Human-readable URLs based on show titles.
* Lightweight HTTP server built into Python.
* Simple YAML configuration.
* Docker-friendly.
* Supports running as an arbitrary UID.

## Installation

### Requirements

* Docker
* Docker Compose

### Build

Clone the repository and build the image.

```bash
docker build -t poddie .
```

### Run and configure

See example docker-compose.yml and config.example.yml (mount to the container as /config/config.yml).

The application will automatically:

1. Download the latest yt-dlp.
2. Check each configured show.
3. Download new episodes.
4. Generate RSS feeds.
5. Generate HTML pages.
6. Serve everything on port 8080.

### Global options

| Option            | Description                       | Default                        |
| ----------------- | --------------------------------- | ------------------------------ |
| `title`           | Website title                     | `Podcasts`                     |
| `description`     | Website description               | empty                          |
| `base_url`        | Public URL of the Poddie instance | required for correct RSS links |
| `update_interval` | Seconds between update runs       | `43200` (12 hours)             |

### Show options

| Option         | Required | Description                                           |
| -------------- | -------- | ----------------------------------------------------- |
| `title`        | Yes      | Show title                                            |
| `url`          | Yes      | URL passed directly to yt-dlp                         |
| `description`  | No       | Description shown on the HTML page and RSS feed       |
| `icon`         | No       | Cover image URL                                       |
| `max_episodes` | No       | Maximum episodes downloaded per update (default `10`) |


## Notes

* Poddie relies entirely on yt-dlp for media extraction.
* Supported websites are therefore those supported by yt-dlp.
* Only newly discovered episodes are downloaded.
* Existing downloads are tracked using yt-dlp's download archive.

## Disclaimer

Use this software at your own risk.

Poddie is a personal project created to solve a practical need for generating podcast feeds from websites that do not natively provide them. It is intentionally simple and prioritises a minimal, maintainable implementation over a large feature set.

Contributions and bug reports are welcome.
