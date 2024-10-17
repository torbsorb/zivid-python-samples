from pathlib import Path

try:
    import importlib.resources as resources
except ImportError:
    import importlib_resources as resources


def get_file_path(file_name: str) -> Path:
    with resources.as_file(resources.files("zividsamples.images") / file_name) as icon_file:
        return Path(icon_file)
