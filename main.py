import argparse
import logging
from pathlib import Path

from waggle.plugin import Plugin


def main(args):
    path = Path(args.dir_path)
    if not path.is_dir():
        logging.error(f"The provided path '{args.dir_path}' is not a valid directory.")
        return 1

    logging.info(f"Starting upload of files from {args.dir_path} with pattern {args.file_pattern}")
    
    pattern = f"**/{args.file_pattern}"
    logging.info(f"'**' is added for recursive search. The pattern used: {pattern}")
    with Plugin() as plugin:
        for filepath in path.glob(pattern):
            logging.info(f"Found file: {filepath}")
            donefile = filepath.with_suffix(".done")
            if donefile.exists():
                logging.info(f"File already uploaded: {filepath}")
                continue

            logging.info(f"Uploading file: {filepath}")
            plugin.upload_file(filepath, keep=args.keep_file)
            logging.info(f"File uploaded: {filepath}. Marking as done.")
            donefile.touch()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Upload files from a directory."
        )
    )
    parser.add_argument(
        "--DEBUG",
        action="store_true",
        help="Enable debug logging."
    )
    parser.add_argument(
        "--dir-path",
        type=str,
        required=True,
        help="Directory path to search for files."
    )
    parser.add_argument(
        "--file-pattern",
        type=str,
        default="**/*.nc",
        help="File pattern to match."
    )
    parser.add_argument(
        "--keep-file",
        action="store_true",
        default=False,
        help="Flag to keep the file after upload."
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.DEBUG else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)

    exit(main(args))