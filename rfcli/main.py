import click
from rich import print
from rfcli.upload import upload_images, upload_dataset
from rfcli.version import create_version
from rfcli.train_local import train_local
from rfcli.predict import predict


@click.group()
@click.version_option("0.1.3", prog_name="RFCLI")
def cli():
    """Roboflow CLI - Dataset to Deployment"""
    pass


# 🔹 Single image upload
@cli.command()
@click.option('--workspace', required=True)
@click.option('--project', required=True)
@click.option('--folder', required=True)
def upload(workspace, project, folder):
    print("[bold blue]🚀 Uploading images...[/bold blue]")
    upload_images(workspace, project, folder)


# 🔥 Dataset upload
@cli.command(name="upload-dataset")
@click.option('--workspace', required=True)
@click.option('--project', required=True)
@click.option('--path', required=True)
def upload_dataset_cmd(workspace, project, path):
    print("[bold blue]🚀 Uploading dataset...[/bold blue]")
    upload_dataset(workspace, project, path)


# 🔥 Create version
@cli.command(name="create-version")
@click.option('--workspace', required=True)
@click.option('--project', required=True)
@click.option('--name', required=True)
def create_version_cmd(workspace, project, name):
    print("[bold blue]🚀 Creating dataset version...[/bold blue]")
    create_version(workspace, project, name)


# 🔥 Train
@cli.command(name="train-local")
@click.option('--workspace', required=True)
@click.option('--project', required=True)
@click.option('--version', required=True, type=int)
def train_local_cmd(workspace, project, version):
    train_local(workspace, project, version)


# 🔥 Predict
@cli.command(name="predict")
@click.option('--image', required=True)
def predict_cmd(image):
    predict(image)


# 🔹 Test command
@cli.command()
def hello():
    print("[bold green]Roboflow CLI is working! 🚀[/bold green]")


if __name__ == "__main__":
    cli()