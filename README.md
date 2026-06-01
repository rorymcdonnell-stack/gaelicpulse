# Gaelic Pulse

The Intelligence Platform for Gaelic Games. Live trackers, county-by-county analysis, and long-form intelligence across Gaelic football, hurling, camogie and ladies football.

**Live site:** [www.gaelicpulse.com](https://www.gaelicpulse.com)

## What this is

A static HTML site published to Netlify. No build step — files are served as-is.

## Structure

```
.
├── index.html                  # Landing page
├── intelligence/               # Pulse Intelligence — long-form analysis
│   ├── index.html              # Section landing
│   └── the-*.html              # Individual pieces
├── football/                   # Football tracker + 32 county pages
├── hurling/                    # Hurling tracker
├── camogie/                    # Camogie tracker
├── ladies-football/            # Ladies football tracker
├── shared/                     # Cross-site CSS (site chrome, county styles)
├── static/                     # Hero images, OG cards, favicons
├── netlify.toml                # Deploy config (redirects, headers)
├── robots.txt
└── sitemap.xml
```

## Editorial mantra

> What happened. Why it happened. What happens next.

## Data principle

Every figure on the site traces to a real fetched result. Real-but-partial beats complete-but-fake. A blank is trustworthy; a confident wrong number is fatal.

## Deploy

Push to `main` — Netlify auto-deploys.
