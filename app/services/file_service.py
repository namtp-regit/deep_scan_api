import shutil
from pathlib import Path
from datetime import datetime


class FileService:
    def __init__(self, upload_dir: str):
        self.upload_dir = Path(upload_dir)
        if not self.upload_dir.exists():
            self.upload_dir.mkdir(parents=True, exist_ok=True)

    def generate_file_name(self, original_name: str) -> str:
        name, ext = Path(original_name).stem, Path(original_name).suffix
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{name}_{timestamp}{ext}"

    def save_file(
        self, file, filename: str = None, subfolder: str = None, timestamp: bool = False
    ) -> str:
        if filename is None:
            filename = file.filename

        # add timestamp to filename
        if timestamp:
            filename = self.generate_file_name(filename)

        # subfolder handling
        target_dir = self.upload_dir
        if subfolder:
            target_dir = target_dir / subfolder
            target_dir.mkdir(parents=True, exist_ok=True)

        file_path = target_dir / filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return str(file_path)

    def get_file_path(self, filename: str, subfolder: str = None) -> str:
        file_path = self.upload_dir
        if subfolder:
            file_path = file_path / subfolder

        file_path = file_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File '{filename}' does not exist")
        return str(file_path)
