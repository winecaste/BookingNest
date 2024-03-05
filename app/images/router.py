from fastapi import APIRouter, UploadFile, Request, File
import shutil

from fastapi.responses import HTMLResponse
from app.pages.router import templates
from app.tasks.tasks import process_pic

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"]
)


@router.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("upload_images.html", {"request": request})


@router.post("/upload-files")
async def add_hotel_image(request: Request, file: UploadFile = File(...)):
    if not file:
        raise
    img_path = f"app/static/images/{file.filename}"
    with open(img_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(img_path)
    return templates.TemplateResponse('success.html', context={'request': request})
