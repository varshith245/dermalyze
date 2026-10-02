import base64
import os
from io import BytesIO

from dotenv import load_dotenv
from groq import Groq
from PIL import Image


load_dotenv()


def encode_image_for_groq(filepath):
    image = Image.open(filepath)
    image.thumbnail((1024, 1024))

    buffer = BytesIO()
    image.convert("RGB").save(buffer, format="JPEG", quality=75)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def extract_video_frames(video_filepath, num_frames=3):
    """
    Extract key frames from a video file using OpenCV.
    Returns a list of base64-encoded JPEG strings and a list of temp file paths.
    """
    import cv2
    import tempfile

    cap = cv2.VideoCapture(video_filepath)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_filepath}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 0:
        cap.release()
        raise ValueError("Video has no readable frames.")

    # Sample frames at evenly spaced positions (20%, 50%, 80%)
    positions = [0.2, 0.5, 0.8]
    if num_frames != 3:
        positions = [i / (num_frames + 1) for i in range(1, num_frames + 1)]

    frame_indices = [int(total_frames * p) for p in positions]

    frames_b64 = []
    frame_paths = []

    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue

        # Convert BGR (OpenCV) to RGB (PIL)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        pil_image.thumbnail((1024, 1024))

        # Save frame to temp file for serving
        temp_file = tempfile.NamedTemporaryFile(
            suffix=".jpg", delete=False, dir=os.path.dirname(video_filepath) or "."
        )
        pil_image.save(temp_file.name, format="JPEG", quality=85)
        frame_paths.append(temp_file.name)

        # Base64 encode for Groq
        buffer = BytesIO()
        pil_image.save(buffer, format="JPEG", quality=75)
        frames_b64.append(base64.b64encode(buffer.getvalue()).decode("utf-8"))

    cap.release()
    return frames_b64, frame_paths


def brain_of_the_doctor(patient_text, image_filepath=None, video_filepath=None):
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("Missing GROQ_API_KEY in .env or environment")

    extracted_frame_paths = []

    # Build multimodal content blocks
    image_contents = []

    if video_filepath:
        # Extract frames from video
        try:
            frames_b64, extracted_frame_paths = extract_video_frames(video_filepath, num_frames=3)
            for frame_b64 in frames_b64:
                image_contents.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{frame_b64}"},
                })
        except Exception as e:
            print(f"Warning: Video frame extraction failed: {e}")
            # Fall through to image if available

    if image_filepath:
        image_data = encode_image_for_groq(image_filepath)
        image_contents.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
        })

    if not image_contents:
        raise ValueError("No visual input provided. Please upload an image or video.")

    # Build prompt
    num_images = len(image_contents)
    source_desc = ""
    if video_filepath and extracted_frame_paths:
        source_desc = f"The patient uploaded a video. {len(extracted_frame_paths)} key frames have been extracted at different time points for your analysis. "
    if image_filepath:
        source_desc += "The patient also uploaded a direct photo. "

    prompt = (
        "You are a professional, empathetic dermatology specialist AI. "
        "Analyze the provided skin image(s) alongside the patient's verbal description. "
        "Provide a thorough, structured consultation response including:\n"
        "1. What you observe in the visual evidence\n"
        "2. Possible considerations (not a diagnosis)\n"
        "3. Recommended self-care steps\n"
        "4. When to see a doctor in person\n\n"
        "Be detailed but clear. Use plain language the patient can understand. "
        "Do not use asterisks, markdown formatting, or special characters as this will be converted to audio.\n\n"
        f"{source_desc}\n"
        f"Patient description: {patient_text}"
    )

    client = Groq(api_key=groq_api_key)
    response = client.chat.completions.create(
        model=os.environ.get("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
        max_completion_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": "You are a careful skin care assistant. Provide thorough general information, not a diagnosis. Structure your response clearly.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    *image_contents,
                ],
            },
        ],
    )

    return response.choices[0].message.content, extracted_frame_paths
