import os
import json
import shutil
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the existing pipeline functions
from src.voice_of_the_patient import transcribe_patient_voice
from src.brain_of_the_doctor_groq import brain_of_the_doctor
from src.voice_of_the_doctor import convert_text_to_doctor_audio

app = FastAPI(title="Dermalyze API")

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
MEDIA_DIR = PROJECT_ROOT / "temp_media"
MEDIA_DIR.mkdir(exist_ok=True)

DB_PATH = PROJECT_ROOT / "consultations.json"

# Read/Write helpers for JSON database
def load_db():
    if not DB_PATH.exists():
        return []
    try:
        with DB_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_db(data):
    with DB_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Helper to save uploaded file
def save_upload(upload_file: UploadFile, extension: str) -> Path:
    temp_id = uuid.uuid4().hex
    file_path = MEDIA_DIR / f"upload_{temp_id}{extension}"
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

# ============ HTML TEMPLATE SERVING ============

def serve_html_file(filename: str) -> HTMLResponse:
    filepath = PROJECT_ROOT / "frontend" / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail=f"{filename} not found")
    with filepath.open("r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.get("/", response_class=HTMLResponse)
def serve_landing():
    return serve_html_file("landing.html")

@app.get("/how-it-works", response_class=HTMLResponse)
def serve_how_it_works():
    return serve_html_file("how-it-works.html")

@app.get("/privacy", response_class=HTMLResponse)
def serve_privacy():
    return serve_html_file("privacy.html")

@app.get("/dashboard", response_class=HTMLResponse)
def serve_dashboard():
    return serve_html_file("dashboard.html")

@app.get("/consultation", response_class=HTMLResponse)
def serve_consultation():
    return serve_html_file("consultation.html")

@app.get("/results/{consultation_id}", response_class=HTMLResponse)
def serve_results(consultation_id: str):
    return serve_html_file("results.html")

# ============ JSON API ENDPOINTS ============

@app.get("/api/consultations")
def get_consultations_history():
    db = load_db()
    # Return sorted by timestamp desc
    return sorted(db, key=lambda x: x.get("timestamp", ""), reverse=True)

@app.get("/api/consultation/{consultation_id}")
def get_consultation_detail(consultation_id: str):
    db = load_db()
    for item in db:
        if item.get("id") == consultation_id:
            return item
    raise HTTPException(status_code=404, detail="Consultation not found")

@app.post("/analyze")
async def analyze_concern(
    audio: UploadFile = File(None),
    transcript_text: str = Form(None),
    image: UploadFile = File(None),
    video: UploadFile = File(None)
):
    # Validate inputs
    if not audio and not transcript_text:
        raise HTTPException(status_code=400, detail="Please provide a voice note description or type your symptoms.")
    
    if not image and not video:
        raise HTTPException(status_code=400, detail="Please upload a skin image or video.")

    # Generate standard metadata
    consultation_id = uuid.uuid4().hex
    timestamp = import_timestamp()
    
    audio_path = None
    if audio and audio.filename:
        audio_path = save_upload(audio, Path(audio.filename).suffix or ".webm")
        
    image_path = None
    if image and image.filename:
        image_path = save_upload(image, Path(image.filename).suffix or ".jpg")
        
    video_path = None
    if video and video.filename:
        video_path = save_upload(video, Path(video.filename).suffix or ".mp4")

    # Transcribe voice or use manual text input
    patient_text = ""
    if audio_path:
        try:
            patient_text = transcribe_patient_voice(str(audio_path))
        except Exception as e:
            print(f"Transcription failed: {e}")
            if transcript_text:
                patient_text = transcript_text
            else:
                raise HTTPException(status_code=500, detail=f"Voice transcription failed: {str(e)}")
    else:
        patient_text = transcript_text

    if not patient_text:
        patient_text = "No description provided."

    # Perform analysis
    try:
        doctor_text, extracted_frames = brain_of_the_doctor(
            patient_text=patient_text,
            image_filepath=str(image_path) if image_path else None,
            video_filepath=str(video_path) if video_path else None
        )
        
        # Generate speech response
        doctor_audio_filename = f"doctor_response_{consultation_id}.mp3"
        doctor_audio_path = MEDIA_DIR / doctor_audio_filename
        convert_text_to_doctor_audio(doctor_text, output_filepath=str(doctor_audio_path))

    except Exception as e:
        # Clean up files in case of error
        for p in [audio_path, image_path, video_path]:
            if p and p.exists():
                try:
                    p.unlink()
                except Exception:
                    pass
        raise HTTPException(status_code=500, detail=f"AI pipeline analysis failed: {str(e)}")

    # Construct final consultation record
    image_url = f"/media/{image_path.name}" if image_path else None
    audio_url = f"/media/{doctor_audio_filename}"
    frame_urls = [f"/media/{Path(frame_path).name}" for frame_path in extracted_frames]
    
    # Save the input video to media if we want to serve it later, or delete
    media_type = "image"
    if video_path:
        media_type = "video"
        # We can keep the video or delete it. Let's delete to save space, keeping the extracted key frames.
        try:
            video_path.unlink()
        except Exception:
            pass

    # Clean up input audio to save space
    if audio_path and audio_path.exists():
        try:
            audio_path.unlink()
        except Exception:
            pass

    # Title extraction for bento grid
    title = "Skin Consultation"
    if "dermatitis" in doctor_text.lower():
        title = "Dermatitis Assessment"
    elif "eczema" in doctor_text.lower():
        title = "Eczema Assessment"
    elif "acne" in doctor_text.lower():
        title = "Acne Assessment"
    elif "mole" in doctor_text.lower() or "nevus" in doctor_text.lower():
        title = "Mole Assessment"

    record = {
        "id": consultation_id,
        "timestamp": timestamp,
        "title": title,
        "transcript": patient_text,
        "doctor_response": doctor_text,
        "image_url": image_url,
        "audio_url": audio_url,
        "media_type": media_type,
        "extracted_frames": frame_urls
    }

    db = load_db()
    db.append(record)
    save_db(db)

    return {"consultation_id": consultation_id}

@app.get("/media/{filename}")
def get_media_file(filename: str):
    file_path = MEDIA_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Media file not found")
    return FileResponse(file_path)

def import_timestamp():
    from datetime import datetime
    return datetime.utcnow().isoformat() + "Z"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=7860, reload=True)
