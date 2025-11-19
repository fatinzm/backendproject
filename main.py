# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from yt_video_fetcher import fetch_and_download_tiktok_videos

app = FastAPI()


class DownloadRequest(BaseModel):
    username: str


@app.get("/")
async def root():
    # Render will call this for health checks.
    # It MUST return 2xx, not 404.
    return {"status": "ok"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/download")
async def download_videos(request: DownloadRequest):
    try:
        video_urls = fetch_and_download_tiktok_videos(request.username)
        return {"status": "success", "video_urls": video_urls}
    except HTTPException:
        # Re-raise our own HTTPExceptions
        raise
    except Exception as e:
        # Any unexpected Python error
        raise HTTPException(status_code=500, detail=str(e))
