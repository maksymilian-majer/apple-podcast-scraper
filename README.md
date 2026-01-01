# Apple Podcast Transcript Scraper

Extract transcripts from Apple Podcasts on macOS to build personal knowledge bases.

## Prerequisites

**Important:** This script extracts transcripts that Apple Podcasts has already cached locally. You must:

1. Use the **Apple Podcasts app on macOS**
2. Open episodes and click the **Transcript** icon to view them first
3. Only then can this script extract the cached transcript files

The script cannot download transcripts directly from Apple - it only reads what's already cached on your Mac.

## Requirements

- macOS with Apple Podcasts app
- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

## Usage

1. Open Apple Podcasts on your Mac
2. Play or browse episodes and click the **Transcript** icon (wait for it to load)
3. Run the script:

```bash
uv run python extract_transcript.py
```

4. Select from the 10 most recent transcripts (or press Enter for the latest)
5. The transcript is saved to `transcript_export.txt`

## Use Cases

- Build knowledge bases from your favorite podcast episodes
- Create custom AI assistants (like Gemini Gems) trained on podcast content
- Quick reference and searchable notes from episodes
- Study material from educational podcasts

## How it works

Apple Podcasts caches transcripts as TTML (Timed Text Markup Language) files in:

```
~/Library/Group Containers/243LU875E5.groups.com.apple.podcasts/Library/Cache/Assets/TTML/
```

The script finds cached TTML files, displays them sorted by date with a preview, and extracts clean text.
