from rich import print
from roboflow import Roboflow
from rfcli.config import get_api_key


def create_version(workspace, project_name, version_name):

    print("[blue]🚀 Creating dataset version with split...[/blue]")

    try:
        rf = Roboflow(api_key=get_api_key())
        project = rf.workspace(workspace).project(project_name)

        # 🔥 Create version with splits
        version = project.generate_version(
            {
                "name": version_name,

                # ✅ SPLIT CONFIG
                "splits": {
                    "train": 70,
                    "valid": 20,
                    "test": 10
                },

                # ✅ PREPROCESSING
                "preprocessing": {
                    "resize": {
                        "width": 640,
                        "height": 640,
                        "format": "Stretch to"
                    }
                },

                # (optional)
                "augmentation": {}
            }
        )

        print("[green]✅ Version created successfully![/green]")
        print(f"[bold]Version Name:[/bold] {version_name}")

        print("\n[cyan]📊 Version Info:[/cyan]")
        print(version)

    except Exception as e:
        print(f"[red]❌ Failed to create version: {str(e)}[/red]")