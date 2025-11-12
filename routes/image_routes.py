from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import List
from fastapi.responses import JSONResponse
from utils.dependencies import get_current_user
import base64

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)

@router.post("/process", summary="Upload 4 images for processing", 
             description="""
Sample request (multipart/form-data):

- images: 4 image files  
- Header: Authorization: Bearer <JWT_TOKEN>
""")
async def process_images(
    images: List[UploadFile] = File(..., description="Upload exactly 4 images"),
    current_user=Depends(get_current_user)
):
    if len(images) != 4:
        raise HTTPException(status_code=400, detail="Exactly 4 images required")

    # Hardcoded logic for now
    is_ok_case = False  # change to True to just return "ok"

    if is_ok_case:
        return {"status": "ok"}
    else:
        # Convert each image to Base64
        processed_images_base64 = []
        for img in images:
            content = await img.read()
            encoded = base64.b64encode(content).decode("utf-8")
            processed_images_base64.append({
                "filename": img.filename,
                "content": encoded
            })
        return JSONResponse(content={"status": "notgood", "images": processed_images_base64})
