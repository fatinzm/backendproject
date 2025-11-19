# TikTok Video Validator Backend

This project downloads the 5 most recent (including pinned) TikTok videos for any username and serves them via a FastAPI backend.

## Features
- Uses undetected_chromedriver to bypass bot detection
- Scrapes TikTok video links and downloads with yt-dlp
- Serves videos via FastAPI `/static`
- Clears old videos before downloading new ones

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
