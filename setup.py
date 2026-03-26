from setuptools import setup, find_packages

setup(
    name="rfcli",
    version="0.1.4",  # 🔥 bump version
    packages=find_packages(),

    install_requires=[
        "click",
        "rich",
        "roboflow",
        "fastapi",
        "uvicorn",
        "python-multipart",
    ],

    extras_require={
        "ml": [
            "ultralytics",
            "torch",
            "opencv-python"
        ]
    },

    entry_points={
        "console_scripts": [
            "rfcli=rfcli.main:cli"
        ]
    },

    author="Saahiti K S",
    description="Dataset-to-Deployment CLI for Object Detection",
    python_requires=">=3.8",
)