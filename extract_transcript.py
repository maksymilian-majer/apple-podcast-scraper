import os
import glob
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime


def get_ttml_base_path():
    """Returns the base path for Apple Podcasts TTML cache."""
    home = str(Path.home())
    return os.path.join(
        home,
        "Library/Group Containers/243LU875E5.groups.com.apple.podcasts/Library/Cache/Assets/TTML",
    )


def get_transcript_files(limit=10):
    """
    Locates TTML files in the Apple Podcasts cache, sorted by modification time.
    Returns up to `limit` most recent files.
    """
    base_path = get_ttml_base_path()

    if not os.path.exists(base_path):
        print(f"Error: Path not found: {base_path}")
        return []

    search_pattern = os.path.join(base_path, "**", "*.ttml")
    files = glob.glob(search_pattern, recursive=True)

    if not files:
        return []

    # Sort by modification time (newest first)
    files_sorted = sorted(files, key=os.path.getmtime, reverse=True)
    return files_sorted[:limit]


def get_preview(file_path, max_words=12):
    """
    Extracts the first few words from a TTML file as a preview.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        words = []
        for elem in root.iter():
            if elem.tag.endswith("}p") or elem.tag == "p":
                for child in elem.iter():
                    unit = child.attrib.get(
                        "{http://podcasts.apple.com/transcript-ttml-internal}unit"
                    )
                    if unit == "word" and child.text:
                        words.append(child.text.strip())
                        if len(words) >= max_words:
                            return " ".join(words) + "..."

        if words:
            return " ".join(words)
        return "(empty transcript)"
    except ET.ParseError:
        return "(parse error)"


def parse_ttml(file_path):
    """
    Parses the TTML XML file and extracts clean text.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        transcript_lines = []

        for elem in root.iter():
            if elem.tag.endswith("}p") or elem.tag == "p":
                words = []
                for child in elem.iter():
                    unit = child.attrib.get(
                        "{http://podcasts.apple.com/transcript-ttml-internal}unit"
                    )
                    if unit == "word" and child.text:
                        words.append(child.text.strip())

                if words:
                    transcript_lines.append(" ".join(words))

        return "\n\n".join(transcript_lines)

    except ET.ParseError as e:
        return f"Error parsing XML: {e}"


def format_file_date(file_path):
    """Returns formatted modification date for a file."""
    mtime = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")


def display_episodes(files):
    """Displays a numbered list of episodes with date and preview."""
    print("\nRecent transcripts:\n")
    print(f"{'#':<3} {'Date':<17} {'Preview'}")
    print("-" * 70)

    for i, file_path in enumerate(files, 1):
        date_str = format_file_date(file_path)
        preview = get_preview(file_path)
        # Truncate preview if too long
        if len(preview) > 45:
            preview = preview[:45] + "..."
        print(f"{i:<3} {date_str:<17} {preview}")

    print()


def get_user_selection(max_num):
    """Prompts user to select an episode number (1-based), default is 1."""
    while True:
        try:
            user_input = input(f"Select episode [1-{max_num}] (default: 1): ").strip()

            if not user_input:
                return 0  # Default to first (index 0)

            selection = int(user_input)
            if 1 <= selection <= max_num:
                return selection - 1  # Convert to 0-based index
            else:
                print(f"Please enter a number between 1 and {max_num}")
        except ValueError:
            print("Please enter a valid number")


def main():
    print("Searching for transcripts in Apple Podcasts cache...")
    files = get_transcript_files(limit=10)

    if not files:
        print("[-] No TTML files found.")
        print(
            "    -> Action Required: Open the 'Transcript' view for an episode in the Apple Podcasts app first."
        )
        return

    display_episodes(files)

    selected_index = get_user_selection(len(files))
    selected_file = files[selected_index]

    print(f"\n[+] Extracting: {os.path.basename(selected_file)}")

    clean_text = parse_ttml(selected_file)

    output_filename = "transcript_export.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(clean_text)

    print(f"[+] Successfully extracted text to '{output_filename}'")

    # Preview
    print("\n--- Preview ---")
    print(clean_text[:300].replace("\n", " ") + "...")


if __name__ == "__main__":
    main()
