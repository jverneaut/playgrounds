#!/usr/bin/env python3
"""Prepare WordPress Playground snapshots for hosting in this repository."""

import argparse
import json
from pathlib import Path
import re
import shutil
import unicodedata
from urllib.parse import quote, urlencode
import zipfile


ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="jverneaut/playgrounds", help="GitHub owner/repository")
    parser.add_argument("--branch", default="main", help="Published Git branch (default: main)")
    args = parser.parse_args()
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", args.repo) or not args.branch.strip():
        parser.error("Provide --repo as owner/repository and a nonempty --branch.")

    source = ROOT / "source"
    source.mkdir(exist_ok=True)
    archives = sorted(p for p in source.iterdir() if p.is_file() and p.suffix.lower() == ".zip")
    if not archives:
        print("Drop exported site ZIP files into source/ and run this script again.")
        return

    # Validate names and archives before replacing any generated files.
    sites = {}
    for archive in archives:
        name = unicodedata.normalize("NFKD", archive.stem).encode("ascii", "ignore").decode()
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        if not slug:
            parser.error(f"Rename {archive.name}: its name must contain letters or numbers.")
        if slug in sites:
            parser.error(f"{archive.name} and {sites[slug].name} both map to {slug}/; rename one.")
        try:
            with zipfile.ZipFile(archive) as snapshot:
                if not snapshot.namelist():
                    parser.error(f"{archive.name} is an empty ZIP.")
        except zipfile.BadZipFile:
            parser.error(f"{archive.name} is not a valid ZIP.")
        sites[slug] = archive

    output = ROOT / "playground"
    raw = f"https://raw.githubusercontent.com/{args.repo}/{quote(args.branch, safe='')}/playground"
    links = [
        "# WordPress Playground demos",
        "",
        "Open a demo in WordPress Playground or view its Blueprint JSON.",
        "Links work after these files are pushed to the public repository.",
        "",
        "| Demo | Playground | Blueprint |",
        "| --- | --- | --- |",
    ]
    for slug, archive in sites.items():
        destination = output / slug
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(archive, destination / "playground.zip")
        blueprint = {
            "$schema": "https://playground.wordpress.net/blueprint-schema.json",
            "landingPage": "/",
            "login": True,
            # Playground URLs aren't localhost, so Jetpack needs explicit offline mode.
            "constants": {"JETPACK_DEV_DEBUG": True},
            "steps": [{
                "step": "importWordPressFiles",
                "wordPressFilesZip": {
                    "resource": "url",
                    "url": f"{raw}/{slug}/playground.zip",
                },
            }],
        }
        (destination / "blueprint.json").write_text(json.dumps(blueprint, indent=2) + "\n", encoding="utf-8")
        for extension in (".jpg", ".jpeg", ".png", ".webp"):
            screenshot = archive.with_suffix(extension)
            if screenshot.is_file():
                shutil.copyfile(screenshot, destination / f"screenshot{extension}")
                break
        blueprint_url = f"{raw}/{slug}/blueprint.json"
        url = "https://playground.wordpress.net/?" + urlencode({"blueprint-url": blueprint_url})
        links.append(f"| **{slug}** | [Open playground]({url}) | [View blueprint JSON]({blueprint_url}) |")
        print(f"{slug}:\n  Playground: {url}\n  Blueprint:  {blueprint_url}")

    (ROOT / "LINKS.md").write_text("\n".join(links) + "\n", encoding="utf-8")
    print("\nPrepared playground/ and LINKS.md. Commit and push them to publish the demos.")


if __name__ == "__main__":
    main()
