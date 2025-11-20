# yt_video_fetcher.py
import os
import subprocess
from typing import List
from fastapi import HTTPException

DOWNLOAD_DIR = "downloads"


def fetch_and_download_tiktok_videos(username: str) -> List[str]:
    """
    Downloads up to 2 recent TikTok videos for a given username using yt-dlp
    and returns the local file paths.
    """

    if not username:
        raise HTTPException(status_code=400, detail="Username is required")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Very simple approach: pass the profile URL to yt-dlp
    profile_url = f"https://www.tiktok.com/@{username}"

    cmd = [
        "yt-dlp",
        profile_url,
        "-o",
        os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),
        "--max-downloads",
        "2",
        "--no-playlist",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail=f"yt-dlp failed (code {result.returncode}): {result.stderr}",
        )

    # Collect downloaded files
    files = [
        os.path.join(DOWNLOAD_DIR, f)
        for f in os.listdir(DOWNLOAD_DIR)
        if os.path.isfile(os.path.join(DOWNLOAD_DIR, f))
    ]

    if not files:
        raise HTTPException(status_code=404, detail="No videos downloaded")

    return files
