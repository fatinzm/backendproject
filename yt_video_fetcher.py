import os
import subprocess
from pathlib import Path

YTDLP_CMD_BASE = [
    "yt-dlp",
    "--no-warnings",
    "--no-progress",
    "--force-ipv4",
    "--extractor-args", "tiktok:player_client=web",  # important for TikTok
]

def download_from_tiktok_profile(username: str, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    # download last 2 videos from profile
    profile_url = f"https://www.tiktok.com/@{username}"

    outtmpl = str(output_dir / "%(id)s.%(ext)s")

    cmd = [
        *YTDLP_CMD_BASE,
        "-o", outtmpl,
        "--max-downloads", "2",
        profile_url,
    ]

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
    )

    if proc.returncode != 0:
        # LOG to server logs
        print("yt-dlp FAILED ---------------------------------")
        print("RETURN CODE:", proc.returncode)
        print("STDERR:\n", proc.stderr)
        print("STDOUT:\n", proc.stdout)
        print("-----------------------------------------------")

        error_output = (proc.stderr or "") + "\n\nSTDOUT:\n" + (proc.stdout or "")
        raise RuntimeError(f"yt-dlp failed (code {proc.returncode}): {error_output}")

    files = []
    for name in os.listdir(output_dir):
        if name.lower().endswith((".mp4", ".mov", ".mkv", ".webm")):
            files.append(output_dir / name)

    return files
