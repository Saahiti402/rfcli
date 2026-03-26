
from rfcli.config import get_api_key

def train_local(workspace, project, version):
    from roboflow import Roboflow
    from ultralytics import YOLO

    print("🚀 Downloading dataset from Roboflow...")

    rf = Roboflow(api_key=get_api_key())
    dataset = rf.workspace(workspace).project(project).version(version).download("yolov8")

    print("✅ Dataset downloaded!")

    print("🚀 Starting YOLO training...")

    model = YOLO("yolov8n.pt")

    model.train(
        data=f"{dataset.location}/data.yaml",
        epochs=50,
        imgsz=640
    )

    print("✅ Training complete!")

    print("📦 Best model saved at:")
    print("runs/detect/train/weights/best.pt")