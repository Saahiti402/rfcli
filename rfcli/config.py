import os


def get_api_key():
    api_key = os.getenv("ROBOFLOW_API_KEY")

    if not api_key:
        raise ValueError(
            "\n❌ ROBOFLOW_API_KEY not set\n\n"
            "👉 Set it using:\n"
            "Windows (PowerShell): setx ROBOFLOW_API_KEY your_key\n"
            "Mac/Linux: export ROBOFLOW_API_KEY=your_key\n"
        )

    return api_key