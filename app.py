from fastapi import FastAPI, UploadFile, File
import shutil
import os
import uuid

# 🔥 Import your CLI functions
from rfcli.upload import upload_dataset
from rfcli.version import create_version
from rfcli.train_local import train_local
from rfcli.predict import predict

app = FastAPI()


@app.get("/")
def home():
    return {"message": "🚀 RFCLI API running"}


# -----------------------------
# 📤 UPLOAD DATASET
# -----------------------------
@app.post("/upload-dataset")
def api_upload_dataset(workspace: str, project: str, path: str):
    upload_dataset(workspace, project, path)
    return {"status": "Dataset uploaded"}


# -----------------------------
# 🧱 CREATE VERSION
# -----------------------------
@app.post("/create-version")
def api_create_version(workspace: str, project: str, name: str):
    create_version(workspace, project, name)
    return {"status": f"Version {name} created"}


# -----------------------------
# 🧠 TRAIN MODEL
# -----------------------------
import threading

@app.post("/train")
def api_train(workspace: str, project: str, version: int):
    
    def run_training():
        train_local(workspace, project, version)

    threading.Thread(target=run_training).start()

    return {"status": "Training started in background"}
# -----------------------------
# 🔍 PREDICT IMAGE
# -----------------------------
@app.post("/predict")
async def api_predict(file: UploadFile = File(...)):

    filename = f"temp_{uuid.uuid4().hex}.jpg"

    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Use your existing predict function
    predict(filename)

    return {"status": "Prediction complete"}