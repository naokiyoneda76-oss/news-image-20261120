"""Grader entrypoint: copy the prebuilt entry.png into the writable output directory."""

import os
import shutil
from pathlib import Path


def main():
    source = Path(__file__).resolve().with_name("entry.png")
    if not source.is_file():
        raise FileNotFoundError(f"Required image is missing: {source} (run draw_image.py to generate it)")

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output_dir / "entry.png")


if __name__ == "__main__":
    main()
