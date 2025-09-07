from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yt_dlp
import os
import uuid

app = FastAPI(title="Instagram Downloader API", version="1.0")

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

class VideoRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "🚀 Instagram Video Downloader API is running"}

@app.post("/download")
def download_video(request: VideoRequest):
    try:
        if not request.url:
            raise HTTPException(status_code=400, detail="No URL provided")

        # Unique filename
        video_id = str(uuid.uuid4())[:8]
        filepath = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.mp4")

        # yt-dlp options
        ydl_opts = {
            "outtmpl": filepath,
            "format": "mp4/best",
        }

        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([request.url])

        # Return video file
        return FileResponse(
            path=filepath,
            filename="video.mp4",
            media_type="video/mp4"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
