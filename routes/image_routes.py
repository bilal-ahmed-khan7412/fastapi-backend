from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from typing import List
from fastapi.responses import JSONResponse
from utils.dependencies import get_current_user
from services.inference import run_batch_inference
from services.image_utils import image_to_base64
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)

@router.post("/process", summary="Upload 4 images for processing", 
             description="""
Sample request (multipart/form-data):

- images: 4 image files  
- model: string (model name)
- Header: Authorization: Bearer <JWT_TOKEN>
""")
async def process_images(
    images: List[UploadFile] = File(..., description="Upload exactly 4 images"),
    model: str = Form(..., description="Model name"),
    current_user=Depends(get_current_user)
):
    if len(images) != 4:
        raise HTTPException(status_code=400, detail="Exactly 4 images required")

    # --- Read all image bytes concurrently ---
    contents = await asyncio.gather(*[img.read() for img in images])

    # --- BATCH YOLO INFERENCE ---
    results = run_batch_inference(contents)  # returns list of 4 results

    final_status = "ok"

    # --- Parallel rendering + base64 encoding ---
    def render_and_encode(result):
        rendered = result.plot()
        return image_to_base64(rendered)

    with ThreadPoolExecutor() as executor:
        output_images_base64 = list(executor.map(render_and_encode, results))

    # --- Prepare final output and check for defects ---
    output_images = []
    for i, result in enumerate(results):
        # Early defect detection
        if len(result.boxes) == 0 or result.masks is None:
            final_status = "notgood"

        output_images.append({
            "filename": images[i].filename,
            "predictions": result.to_json(),
            "visualized": output_images_base64[i]
        })

    return JSONResponse({
        "status": final_status,
        "model": model,
        "images": output_images
    })
