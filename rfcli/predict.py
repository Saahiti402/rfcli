
import cv2
import os


def predict(image_path):
    from ultralytics import YOLO

    print("🚀 Running inference...")

    model = YOLO("runs/detect/train/weights/best.pt")

    results = model(image_path)

    for r in results:
        boxes = r.boxes

        for box in boxes:
            print(f"Detected class: {int(box.cls[0])}, Confidence: {float(box.conf[0]):.2f}")

    # 🔥 Save output instead of showing
    annotated = results[0].plot()

    output_path = "prediction.jpg"
    cv2.imwrite(output_path, annotated)

    print(f"\n✅ Prediction saved at: {os.path.abspath(output_path)}")