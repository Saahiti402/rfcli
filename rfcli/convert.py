import os
import json


def coco_to_yolo(json_path, dataset_path):

    labels_dir = os.path.join(dataset_path, "labels")
    os.makedirs(labels_dir, exist_ok=True)

    with open(json_path) as f:
        data = json.load(f)

    images = {img["id"]: img for img in data["images"]}
    annotations = data["annotations"]

    categories = data["categories"]
    cat_map = {cat["id"]: i for i, cat in enumerate(categories)}

    ann_by_image = {}

    for ann in annotations:
        ann_by_image.setdefault(ann["image_id"], []).append(ann)

    for img_id, img_data in images.items():

        file_name = img_data["file_name"]
        width = float(img_data["width"])
        height = float(img_data["height"])

        label_path = os.path.join(
            labels_dir,
            os.path.splitext(file_name)[0] + ".txt"
        )

        with open(label_path, "w") as f:

            for ann in ann_by_image.get(img_id, []):

                # 🔥 FIX: ensure numeric
                x, y, w, h = map(float, ann["bbox"])

                x_center = (x + w / 2) / width
                y_center = (y + h / 2) / height
                w /= width
                h /= height

                class_id = cat_map[ann["category_id"]]

                f.write(f"{class_id} {x_center} {y_center} {w} {h}\n")

    print("✅ COCO → YOLO conversion complete!")