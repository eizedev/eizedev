# AGENTS.md

This repository is my GitHub profile (`README.md`, shown on github.com/eizedev) and the source of
the landing page on [eize.dev](https://eize.dev), published with GitHub Pages.

## Layout

- `projects.toml` - the one list of my projects: order, groups, texts, badges, the pivotkit block.
  The page and the projects part of `README.md` are generated from it.
- `site/build.py` - the generator (Python, run with uv; its dependencies are declared inline).
- `site/page.html`, `site/style.css` - page shell and styles. The CSS is inlined into the page.
- Besides `index.html` the build writes `llms.txt` (for language models), `sitemap.xml`, `robots.txt`,
  the favicons and the social preview; the page carries schema.org data (JSON-LD) and Open Graph tags.
- `README.md` - hand-written header and gists; everything between `<!-- projects:start ... -->` and
  `<!-- projects:end -->` is generated.
- `logo/` - the two wordmarks the README shows. The logo kit, project icons and favicons live in
  [eizedev/brand](https://github.com/eizedev/brand); the page reads them from there when it is built.
- `.github/workflows/site.yml` - checks the README on pull requests; builds and publishes the page
  on `main`, weekly and by hand.

## Commands

```sh
uv run site/build.py                   # build the page into _site/ (needs network)
uv run site/build.py --readme          # rewrite the generated part of README.md (offline)
uv run site/build.py --check-readme    # what CI runs
python3 -m http.server -d _site        # look at the page
```

## Rules

- Change projects in `projects.toml`, then run `--readme` and commit both. Never edit the generated
  part of `README.md` by hand.
- The page stays static: no JavaScript, no external fonts, scripts, analytics or cookies, nothing
  loaded from another host at view time. Its Content-Security-Policy allows only images from the
  site and the inline stylesheet by hash, so inline `style` attributes do not work; put styles into
  `site/style.css`.
- Light and dark come from `prefers-color-scheme`; check both and a phone width (390 px).
- Versions and stars are read from shields.io at build time. A missing value only drops that value
  from the page; a missing icon or screenshot fails the build so a broken page is never published.
- Public text: no hostnames, addresses or details of my home setup.

## Exceptions to the repository standards

- No CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md or CODEOWNERS: a profile, not a product others contribute to.
- No issue or pull request templates: issues and outside pull requests are not expected here.
- No CHANGELOG.md: the page and README describe the current state; history is in git.
- No docs website and no own social preview or brand folder: eize.dev is the page itself and uses the eizedev logo kit from eizedev/brand.
