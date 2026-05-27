"""Render each *.svg next to this script to matching .png using Chrome headless."""
from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import tempfile

HERE = pathlib.Path(__file__).resolve().parent


def chrome_exe() -> pathlib.Path:
    roots = [
        pathlib.Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        pathlib.Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        pathlib.Path.home() / r"AppData\Local\Google\Chrome\Application\chrome.exe",
    ]
    for p in roots:
        if p.is_file():
            return p
    raise FileNotFoundError("Install Google Chrome or set CHROME_PATH")


def dims(svg: str) -> tuple[int, int]:
    mw = re.search(r'width="(\d+)"', svg)
    mh = re.search(r'height="(\d+)"', svg)
    if not mw or not mh:
        raise ValueError("missing width/height")
    return int(mw.group(1)) + 48, int(mh.group(1)) + 48


def main() -> None:
    import os

    chrome_bin = pathlib.Path(os.environ["CHROME_PATH"]) if os.environ.get("CHROME_PATH") else chrome_exe()

    for svg_path in sorted(HERE.glob("*.svg")):
        svg = svg_path.read_text(encoding="utf-8")
        w, h = dims(svg)
        html = (
            '<!DOCTYPE html>\n<meta charset="UTF-8">\n'
            "<style>html,body{margin:0;background:#0b0f1a;}#wrap{display:inline-block;padding:16px}</style>\n"
            f"<div id=wrap>\n{svg}\n</div>\n"
        )
        with tempfile.TemporaryDirectory() as td:
            tdir = pathlib.Path(td)
            html_path = tdir / "page.html"
            html_path.write_text(html, encoding="utf-8")
            uri = html_path.resolve().as_uri()
            png_path = svg_path.with_suffix(".png")
            cmd = [
                str(chrome_bin),
                "--headless=new",
                "--disable-gpu",
                f"--screenshot={png_path}",
                f"--window-size={w},{h}",
                "--hide-scrollbars",
                "--virtual-time-budget=3000",
                uri,
            ]
            subprocess.run(cmd, check=True, timeout=120)
        size = png_path.stat().st_size
        print(f"OK {png_path.name} {size} bytes")


if __name__ == "__main__":
    main()
