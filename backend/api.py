import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException,
)
from fastapi.middleware.cors import CORSMiddleware

import numpy as np
import cv2
import logging

from backend.web_scan_state import ScanState
from backend.web_solver import solve_from_scanned_faces


from scanner.face_detector import extract_face_stickers
from scanner.color_detector import classify_colors


# --------------------
# Setup
# --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI(title="Rubik's Cube Solver API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scan_state = ScanState()


# --------------------
# Routes
# --------------------
@app.get("/")
def root():
    return {"status": "Rubik's Cube Solver API running"}


@app.post("/reset")
def reset_scan():
    scan_state.reset()
    logger.info("Scan state reset")
    return {"message": "Scan reset successful"}


@app.post("/scan_face")
async def scan_face(
    face: str = Form(...),          # F / R / B / L / U / D
    image: UploadFile = File(...)
):
    if face not in ["F", "R", "B", "L", "U", "D"]:
        raise HTTPException(status_code=400, detail="Invalid face name")

    try:
        contents = await image.read()
        np_arr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image data")

        sticker_images = extract_face_stickers(img)

        if sticker_images is None or len(sticker_images) != 9:
            raise HTTPException(
                status_code=400,
                detail="Could not detect 9 stickers",
            )

        detected_colors = []
        for sticker in sticker_images:
            color = classify_colors(sticker, scan_state.colors_cfg)
            detected_colors.append(color)

        scan_state.set_face(face, detected_colors)
        logger.info(f"Scanned face {face}: {detected_colors}")

        return {
            "message": f"Face {face} scanned successfully",
            "colors": detected_colors,
            "faces_scanned": scan_state.faces_scanned(),
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error in /scan_face")
        raise HTTPException(status_code=500, detail="Internal scan error")


@app.post("/solve")
def solve_cube():
    if not scan_state.is_complete():
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Cube not fully scanned",
                "faces_scanned": scan_state.faces_scanned(),
            },
        )

    solution = solve_from_scanned_faces(scan_state)

    return {
        "status": "success",
        "solution": solution,
    }
