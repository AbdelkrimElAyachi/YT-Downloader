"""
Handle CLI flags mode — allows one-line command usage with arguments.

Usage:
    python app.py --url="https://youtube.com/watch?v=..." --type=audio --output=./downloads --filename=song
"""

import argparse
import os

from utils import Downloader
from cli.cli_styles import print_s
from cli.cli_animations import LoadingAnimation

STREAM_TYPES = ("audio", "video", "progressive")


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser for CLI flags mode."""
    parser = argparse.ArgumentParser(
        prog="yt-downloader",
        description="Download YouTube audio/video streams from the command line.",
    )
    parser.add_argument(
        "--url",
        required=True,
        help="YouTube video URL",
    )
    parser.add_argument(
        "--type",
        choices=STREAM_TYPES,
        default="progressive",
        help="Stream type to download (default: progressive)",
    )
    parser.add_argument(
        "--output",
        default=os.getcwd(),
        help="Output directory (default: current directory)",
    )
    parser.add_argument(
        "--filename",
        default=None,
        help="Output filename (extension is added automatically)",
    )
    parser.add_argument(
        "--itag",
        type=int,
        default=None,
        help="Specific itag to download. If omitted, the best stream of the chosen type is used.",
    )
    return parser


def run_cli_flags_mode():
    """Parse CLI arguments and perform the download."""
    parser = build_parser()
    args = parser.parse_args()

    # --- Create downloader ---
    try:
        downloader = Downloader(args.url)
    except ValueError as e:
        print_s(f"Error: {e}", color="RED", style="BOLD")
        return

    # --- Resolve streams ---
    filter_kwargs = {
        "audio": {"only_audio": True},
        "video": {"only_video": True},
        "progressive": {"progressive": True},
    }
    streams = downloader.get_streams(**filter_kwargs[args.type])

    if not streams:
        print_s(f"No {args.type} streams found for this video.", color="RED")
        return

    # --- Pick stream ---
    if args.itag:
        stream = next((s for s in streams if s.itag == args.itag), None)
        if not stream:
            print_s(f"No stream found with itag {args.itag}.", color="RED")
            return
    else:
        # Pick the best (first) stream
        stream = streams[0]

    # --- Download ---
    output_path = os.path.expanduser(args.output)

    try:
        with LoadingAnimation("Downloading... ") as load:
            load.switch_to_spinner()
            file_path = downloader.download_stream(
                itag=stream.itag,
                output_path=output_path,
                filename=args.filename,
            )
    except RuntimeError as e:
        print_s(f"\nDOWNLOAD FAILED: {e}\n", color="RED", style="BOLD")
        return

    if file_path:
        print_s(f"Downloaded successfully: {file_path}", color="GREEN")
    else:
        print_s("\nDOWNLOAD FAILED !!!\n", color="RED", style="BOLD")
