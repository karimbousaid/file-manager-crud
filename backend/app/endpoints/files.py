import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.file import FileModel
from ..authentification.auth import verify_token

router = APIRouter(
    tags=["File Manager CRUD"]
)

UPLOAD_DIR = "uploads"
ALLOWED_TYPES = ["application/pdf", "text/plain"]
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create
@router.post("/files")
def upload_file(file: UploadFile = File(...), username: str = Depends(verify_token), db: Session = Depends(get_db)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="File type not allowed")
    filepath = f"{UPLOAD_DIR}/{file.filename}"
    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())
    db_file = FileModel(filename=file.filename, filepath=filepath, owner_username=username)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

# Read
@router.get("/files")
def get_files(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    return db.query(FileModel).filter(FileModel.owner_username == username).all()

# Delete
@router.delete("/files/{file_id}")
def delete_file(file_id: int, username: str = Depends(verify_token), db: Session = Depends(get_db)):
    file = db.query(FileModel).filter(FileModel.id == file_id, FileModel.owner_username == username).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    os.remove(file.filepath)
    db.delete(file)
    db.commit()
    return {"message": "File deleted successfully"}

# request bodies for update
class FileUpdateRequest(BaseModel):
    new_name: str

# Update
@router.put("/files/{file_id}")
def update_file(
    file_id: int,
    request: FileUpdateRequest,
    username: str = Depends(verify_token),
    db: Session = Depends(get_db)
    ):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_username == username
    ).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    old_path = file.filepath
    new_path = f"{UPLOAD_DIR}/{request.new_name}"

    if os.path.exists(old_path):
        os.rename(old_path, new_path)

    # Update DB
    file.filename = request.new_name
    file.filepath = new_path

    db.commit()
    db.refresh(file)
    return file