import os, shutil

async def save_uploaded_file(file, folder="uploaded_files"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, file.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return path
