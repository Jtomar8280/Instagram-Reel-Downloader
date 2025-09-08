from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import yt_dlp
import os
import uuid

app = FastAPI(title="Instagram Reel Downloader API", version="3.0")

# Folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")
STATIC_FOLDER = os.path.join(BASE_DIR, "static")
TEMPLATES_FOLDER = os.path.join(BASE_DIR, "templates")

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")

# Templates
templates = Jinja2Templates(directory=TEMPLATES_FOLDER)

# Request model
class ReelRequest(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_reel")
def get_reel(request: ReelRequest):
    reel_url = request.url

    if not reel_url or "instagram.com/reel/" not in reel_url:
        raise HTTPException(status_code=400, detail="Invalid Instagram Reel URL")

    try:
        # Unique filename
        video_id = str(uuid.uuid4())[:8]
        file_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.mp4")

        # yt-dlp options
        ydl_opts = {
            "outtmpl": file_path,
            "format": "mp4/best",
            "quiet": True
        }

        # Download video directly
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([reel_url])

        # Return video file path (so frontend can preview + download)
        return {"video_url": f"/download/{video_id}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception occurred: {str(e)}")

@app.get("/download/{video_id}")
def download_video(video_id: str):
    file_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.mp4")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(path=file_path, media_type="video/mp4", filename=f"{video_id}.mp4")


