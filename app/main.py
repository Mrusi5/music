from urllib.parse import parse_qs, urlparse
from uuid import uuid4
from fastapi import FastAPI, HTTPException, File, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from subprocess import run
from . database import User, Recording, SessionLocal

import os

if not os.path.isdir("music"):
     os.mkdir("music")
if not os.path.isdir("music/wav"):
     os.mkdir("music/wav")
if not os.path.isdir("music/mp3"):
     os.mkdir("music/mp3")          

app = FastAPI()

class UserCreateRequest(BaseModel):
    name: str

class UserCreateResponse(BaseModel):
    user_id: int
    access_token: str

@app.post("/users", response_model=UserCreateResponse)
def create_user(request: UserCreateRequest):
    name = request.name
    session = SessionLocal()
    access_token = str(uuid4())
    user = User(name=name, access_token=access_token)
    session.add(user)
    session.commit()
    return {"user_id": user.id, "access_token": access_token}

class RecordingCreateResponse(BaseModel):
    url: str

@app.post("/users/{user_id}/recordings", response_model=RecordingCreateResponse)
def upload_recording(user_id: int, access_token: str, file: bytes = File()):
    session = SessionLocal()
    user = session.query(User).get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if access_token not in user.access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    # Сохранение аудиозаписи на хост-машине
    recording_id = str(uuid4())
    local_path = f"music/wav/{recording_id}.wav"
    with open(local_path, "wb") as f:
        f.write(file)
    # Преобразование аудиозаписи в формат mp3
    mp3_path = f"music/mp3/{recording_id}.mp3"
    run(["ffmpeg", "-i", local_path, "-codec:a", "libmp3lame", "-qscale:a", "2", mp3_path])
    # Сохранение информации об аудиозаписи в базе данных
    recording = Recording(id=recording_id, path=mp3_path, user_id=user_id)
    session.add(recording)
    session.commit()
    # Возвращаем URL для скачивания аудиозаписи
    return {"url": f"http://localhost:8000/recordings/{recording_id}?user_id={user_id}&access_token={access_token}"}

@app.get("/recordings/{recording_id}")
def download_recording(url: str):
    session = SessionLocal()
    url_parts = urlparse(url)

    recording_id = url_parts.path.split("/")[-1]
    query_params = parse_qs(url_parts.query)
    user_id = int(query_params['user_id'][0])
    access_token = query_params['access_token'][0]
    user = session.query(User).get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if access_token not in user.access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    recording = session.query(Recording).get(recording_id)
    if recording is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recording not found")
    # Отправляем аудиозапись как streaming response
    return FileResponse(recording.path, filename=f"{recording_id}.mp3", media_type="audio/mpeg")