# Apple Podcast Transcript Scraper

Extract transcripts from Apple Podcasts on macOS.

## Requirements

- macOS with Apple Podcasts app
- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

## Usage

1. Open Apple Podcasts on your Mac
2. Click the **Transcript** icon on any episode (wait for it to load)
3. Run the script:

```bash
uv run python extract_transcript.py
```

4. The transcript is saved to `transcript_export.txt`

## How it works

Apple Podcasts caches transcripts as TTML (Timed Text Markup Language) files in:

```
~/Library/Group Containers/243LU875E5.groups.com.apple.podcasts/Library/Cache/Assets/TTML/
```

The script finds the most recently modified TTML file and extracts the text content.
