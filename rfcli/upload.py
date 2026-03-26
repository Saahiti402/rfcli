import os
from rich import print
from roboflow import Roboflow
from rfcli.config import get_api_key
from rfcli.convert import coco_to_yolo


# -----------------------------
# 🔹 SINGLE IMAGE UPLOAD
# -----------------------------
def upload_images(workspace, project_name, folder_path):

    rf = Roboflow(api_key=get_api_key())
    project = rf.workspace(workspace).project(project_name)

    images = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    print(f"[blue]Uploading {len(images)} images...[/blue]")

    for i, img_name in enumerate(images):
        try:
            project.upload(os.path.join(folder_path, img_name))
            if i % 50 == 0:
                print(f"[green]{i} uploaded...[/green]")
        except Exception as e:
            print(f"[red]Failed {img_name}: {e}[/red]")


# -----------------------------
# 🔥 MAIN DATASET UPLOAD
# -----------------------------
def upload_dataset(workspace, project_name, dataset_path):

    print("[blue]🚀 Initializing Roboflow SDK...[/blue]")

    rf = Roboflow(api_key=get_api_key())
    project = rf.workspace(workspace).project(project_name)

    if not os.path.exists(dataset_path):
        print("[red]❌ Invalid dataset path[/red]")
        return

    # 🔥 CASE 1: SPLIT DATASET
    splits = ["train", "valid", "test"]
    split_exists = any(os.path.exists(os.path.join(dataset_path, s)) for s in splits)

    if split_exists:
        print("[cyan]📂 Detected SPLIT dataset[/cyan]")
        _handle_split_dataset(project, dataset_path)
        return

    # 🔥 CASE 2: COCO JSON in root
    json_files = [f for f in os.listdir(dataset_path) if f.endswith(".json")]

    if json_files:
        print("[cyan]📦 Detected COCO dataset[/cyan]")

        json_path = os.path.join(dataset_path, json_files[0])
        coco_to_yolo(json_path, dataset_path)

    # 🔥 CASE 3: YOLO FLAT DATASET
    print("[cyan]📁 Detected YOLO flat dataset[/cyan]")
    _handle_flat_dataset(project, dataset_path)


# -----------------------------
# 📂 HANDLE SPLIT DATASET
# -----------------------------
def _handle_split_dataset(project, dataset_path):

    splits = ["train", "valid", "test"]

    success, fail = 0, 0

    for split in splits:

        split_path = os.path.join(dataset_path, split)

        if not os.path.exists(split_path):
            continue

        print(f"\n[bold cyan]Processing {split}...[/bold cyan]")

        # Convert COCO if exists
        json_files = [f for f in os.listdir(split_path) if f.endswith(".json")]
        if json_files:
            coco_to_yolo(os.path.join(split_path, json_files[0]), split_path)

        labels_dir = os.path.join(split_path, "labels")

        images = [f for f in os.listdir(split_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

        for i, img_name in enumerate(images):

            img_path = os.path.join(split_path, img_name)
            label_path = os.path.join(labels_dir, os.path.splitext(img_name)[0] + ".txt")

            try:
                if os.path.exists(label_path):
                    project.upload(img_path, annotation_path=label_path, split=split)
                else:
                    project.upload(img_path, split=split)

                success += 1

                if success % 10 == 0:
                    print(f"[green]{success} uploaded...[/green]")

            except Exception as e:
                print(f"[red]Failed {img_name}: {e}[/red]")
                fail += 1

    print(f"\n[bold]Done → Success: {success}, Failed: {fail}[/bold]")


# -----------------------------
# 📁 HANDLE FLAT DATASET
# -----------------------------
def _handle_flat_dataset(project, dataset_path):

    images = [f for f in os.listdir(dataset_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    labels_dir = os.path.join(dataset_path, "labels")

    success, fail = 0, 0

    for i, img_name in enumerate(images):

        img_path = os.path.join(dataset_path, img_name)
        label_path = os.path.join(labels_dir, os.path.splitext(img_name)[0] + ".txt")

        try:
            if os.path.exists(label_path):
                project.upload(img_path, annotation_path=label_path, split="train")
            else:
                project.upload(img_path)

            success += 1

            if success % 100 == 0:
                print(f"[green]{success} uploaded...[/green]")

        except Exception as e:
            print(f"[red]Failed {img_name}: {e}[/red]")
            fail += 1

    print(f"\n[bold]Done → Success: {success}, Failed: {fail}[/bold]")