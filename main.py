# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from yt_video_fetcher import fetch_and_download_tiktok_videos

app = FastAPI()


class DownloadRequest(BaseModel):
    username: str


@app.get("/")
async def root():
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
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

