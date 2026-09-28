from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path
import shutil
import uuid

from ml.taste_drift_pipeline import analyze_user
from ml.analyze_letterboxd import analyze_letterboxd
from ml.analyze_netflix import analyze_netflix


app = FastAPI(
    title="Taste Drift API",
    description="Backend API for Taste Drift",
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "data" / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================================
# BASIC ROUTES
# =========================================================

@app.get("/")
def root():
    return {
        "message": "Taste Drift API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================================================
# MOVIELENS DEMO ANALYSIS
# =========================================================

@app.get("/analyze/{user_id}")
def analyze(
    user_id: int,
    periods: int = 6,
):
    results = analyze_user(
        user_id=user_id,
        periods=periods,
    )

    if results is None:
        raise HTTPException(
            status_code=404,
            detail="User could not be analyzed.",
        )

    return {
        "success": True,
        "user_id": user_id,
        "periods": periods,
        "analysis": results,
    }


# =========================================================
# ARCHIVE UPLOAD + ANALYSIS
# =========================================================

@app.post("/upload-archive")
async def upload_archive(
    source: str = Form(...),
    file: UploadFile = File(...),
):
    source = source.lower().strip()

    if source not in {
        "letterboxd",
        "netflix",
    }:
        raise HTTPException(
            status_code=400,
            detail="Unsupported archive source.",
        )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was selected.",
        )

    suffix = Path(file.filename).suffix.lower()

    if source == "letterboxd":
        allowed_extensions = {
            ".csv",
            ".zip",
        }

    else:
        allowed_extensions = {
            ".csv",
        }

    if suffix not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type for {source}.",
        )

    unique_name = (
        f"{source}_"
        f"{uuid.uuid4().hex}"
        f"{suffix}"
    )

    destination = (
        UPLOAD_DIR / unique_name
    )

    # -----------------------------------------
    # SAVE FILE
    # -----------------------------------------

    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

    finally:
        await file.close()


    # =====================================================
    # LETTERBOXD
    # =====================================================

    if source == "letterboxd":

        if suffix == ".zip":
            return {
                "success": True,
                "uploaded": True,
                "analyzed": False,
                "message":
                    "Letterboxd ZIP uploaded. ZIP parsing is not implemented yet.",
                "stored_filename":
                    unique_name,
            }

        try:
            analysis = analyze_letterboxd(
                destination,
                periods=4,
            )

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=(
                    "Letterboxd analysis failed: "
                    + str(error)
                ),
            )

        if not analysis.get("success"):
            raise HTTPException(
                status_code=400,
                detail=analysis.get(
                    "message",
                    "Letterboxd analysis failed.",
                ),
            )

        return {
            "success": True,
            "uploaded": True,
            "analyzed": True,

            "message":
                "Letterboxd archive analyzed successfully.",

            "source":
                source,

            "original_filename":
                file.filename,

            "stored_filename":
                unique_name,

            "analysis":
                analysis,
        }


    # =====================================================
    # NETFLIX
    # =====================================================

    if source == "netflix":

        try:
            analysis = analyze_netflix(
                destination,
                periods=4,
            )

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=(
                    "Netflix analysis failed: "
                    + str(error)
                ),
            )

        if not analysis.get("success"):
            raise HTTPException(
                status_code=400,
                detail=analysis.get(
                    "message",
                    "Netflix analysis failed.",
                ),
            )

        return {
            "success": True,
            "uploaded": True,
            "analyzed": True,

            "message":
                "Netflix archive analyzed successfully.",

            "source":
                source,

            "original_filename":
                file.filename,

            "stored_filename":
                unique_name,

            "analysis":
                analysis,
        }