# WordPress Playground demos

1. Export each site from the builder using **Export → WordPress Playground**.
2. Drop the snapshot ZIP into `source/`, naming it after the demo (for example,
   `coastal-hotel.zip`). Optionally add `coastal-hotel.jpg`, `.jpeg`, `.png`, or
   `.webp` beside it for the showcase screenshot.
3. Run with Python 3; no dependencies are required:

   ```sh
   python3 prepare.py
   ```

4. Commit and push `playground/` and `LINKS.md` to this public repository's `main`
   branch. `LINKS.md` lists each demo with an **Open playground** link and a
   **View blueprint JSON** link. Copy the article links from there and check each
   demo in a private browser window, including navigation, images, and editing.

For example, `source/coastal-hotel.zip` produces:

```text
playground/coastal-hotel/
├── playground.zip
├── blueprint.json
└── screenshot.jpg     # if supplied
```

Names become lowercase folder slugs (`Coastal Hotel.zip` → `coastal-hotel`).
Rerunning updates matching ZIPs, Blueprints, and supplied screenshots. Source
files stay in place and are ignored by Git. Old demo folders are never deleted;
`LINKS.md` lists the ZIPs currently in `source/`. Remove obsolete demo folders or
screenshots manually.

The script uses `jverneaut/playgrounds` and `main` by default. Override them with:

```sh
python3 prepare.py --repo another-owner/playgrounds --branch demos
```

Use exported **site snapshots**, not the builder's internal `blueprint.zip`
bundles. The generated Blueprint restores the snapshot with
[`importWordPressFiles`](https://developer.wordpress.org/playground/handbook/guides/providing-content-for-your-demo/#importwordpressfiles),
opens the homepage, and enables automatic login. Launch links use the documented
[`blueprint-url` parameter](https://developer.wordpress.org/playground/blueprints/using-blueprints/#load-blueprint-from-a-url)
with public GitHub raw URLs. Files must be pushed before those links work; the
script prepares local files and does not publish them. GitHub Pages is not needed.

Blueprints enable [Jetpack Offline Mode](https://jetpack.com/support/offline-mode/)
with `JETPACK_DEV_DEBUG`. This keeps included modules such as Forms working when
a snapshot moves from `localhost` to a Playground URL without a WordPress.com
connection. Plugin files and activation settings still come from the snapshot.
