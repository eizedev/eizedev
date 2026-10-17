# eizedev logo

The mark is `❯e_`: a shell prompt, the "e" of eizedev and a cursor. Colours follow the One Dark palette used in the profile README.

| Colour | Dark background | Light background |
| :-- | :-- | :-- |
| Background | `#272e3d` | `#ffffff` |
| Prompt `❯` | `#98c379` | `#50a14f` |
| `e` | `#61afef` | `#4078f2` |
| Cursor `_` | `#e5c07b` | `#c18401` |

All lettering is converted to paths (Menlo Bold), so the SVGs render the same everywhere without the font installed.

`overview.png` shows every variant at a glance, including the round crop at 240/96/40/20 px on light and dark backgrounds.

## Which file for what

| Use | File |
| :-- | :-- |
| Profile picture (GitHub, Gravatar, LinkedIn, forums, chat) | `png/avatar-500.png` or `png/avatar-1000.png` — square, safe for round crops |
| App-style icon, rounded corners | `png/icon-rounded-512.png` / `-1024.png`, `svg/icon-rounded.svg` |
| Mark without background | `svg/mark-on-dark.svg`, `svg/mark-on-light.svg` and PNGs in 256/512/1024 |
| Single colour (stamps, print, watermark) | `svg/mark-mono-dark.svg`, `svg/mark-mono-white.svg` |
| Name as logo (headers, slides, docs) | `svg/wordmark-on-dark.svg`, `svg/wordmark-on-light.svg`, `png/*@2x.png` |
| Repository social preview / Open Graph | `png/social-preview-1280x640.png` (GitHub: repo Settings → Social preview) |
| Website | `favicon/` — `favicon.svg`, `favicon.ico` (16/32/48), `apple-touch-icon.png` (180), `icon-192/512.png`, `site.webmanifest` |

Website head:

```html
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

## Rebuilding

`source/build.py` regenerates every file in this folder and `source/overview.py` the contact sheet; both write next to themselves, independent of the working directory:

```sh
python3 logo/source/build.py && python3 logo/source/overview.py
```

They need `rsvg-convert` (`brew install librsvg`), Python with `fonttools` and `pillow`, and macOS for `/System/Library/Fonts/Menlo.ttc`.
