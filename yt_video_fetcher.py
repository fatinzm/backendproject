import os
import subprocess
import glob
from fastapi import HTTPException


def download_latest_tiktok_videos(username: str, output_dir: str = "downloads"):
    """
    Download up to 5 latest TikTok videos for a profile using yt-dlp only.
    Raises HTTPException with readable error if yt-dlp fails.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Remove old videos for this user
    for old_file in glob.glob(os.path.join(output_dir, f"{username}_video_*.mp4")):
        try:
            os.remove(old_file)
        except OSError:
            pass

    profile_url = f"https://www.tiktok.com/@{username}"

    tmp_pattern = os.path.join(output_dir, f"{username}_%(id)s.%(ext)s")

    cmd = [
        "python", "-m", "yt_dlp",        # use the module explicitly
        "--no-playlist",
        "--max-downloads", "5",
        "-o", tmp_pattern,
        profile_url,
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        # python not found / weird env
        raise HTTPException(
            status_code=500,
            detail="yt-dlp not available in the runtime environment.",
        )

    if result.returncode != 0:
        # Bubble up the real yt-dlp error message
        raise HTTPException(
            status_code=500,
            detail=f"yt-dlp failed (code {result.returncode}): {result.stderr.strip()}",
        )

    # Rename to pattern expected by main.py
    downloaded = sorted(glob.glob(os.path.join(output_dir, f"{username}_*.mp4")))
    for idx, path in enumerate(downloaded[:5]):
        new_path = os.path.join(output_dir, f"{username}_video_{idx}.mp4")
        if path != new_path:
            os.replace(path, new_path)
