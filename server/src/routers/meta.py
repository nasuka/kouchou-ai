import json
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.schemas.metadata import Metadata

router = APIRouter()
CUSTOM_META_DIR = Path(__file__).parent.parent.parent / "public" / "meta" / "custom"
DEFAULT_META_DIR = Path(__file__).parent.parent.parent / "public" / "meta" / "default"


def load_metadata_file_path(filename: str) -> Path:
    """メタデータファイルのパスを返す。customファイルが存在する場合はcustomファイルを読み、存在しない場合はdefaultファイルを読む"""
    custom_metadata_path = CUSTOM_META_DIR / filename
    metadata_path = custom_metadata_path if custom_metadata_path.exists() else DEFAULT_META_DIR / filename
    return metadata_path


@router.get("/meta")
async def get_metadata() -> Metadata:
    metadata_path = load_metadata_file_path("metadata.json")
    with open(metadata_path) as f:
        metadata = json.load(f)

    return Metadata(
        reporter=metadata["reporter"],
        message=metadata["message"],
        webLink=metadata["webLink"],
        privacyLink=metadata["privacyLink"],
        termsLink=metadata["termsLink"],
        brandColor=metadata["brandColor"],
    )


@router.get("/meta/reporter.png")
async def get_reporter_image():
    return FileResponse(load_metadata_file_path("reporter.png"))


@router.get("/meta/icon.png")
async def get_icon():
    return FileResponse(load_metadata_file_path("icon.png"))


@router.get("/meta/ogp.png")
async def get_ogp():
    return FileResponse(load_metadata_file_path("ogp.png"))


@router.get("/meta/metadata.json")
async def get_metadata_json():
    return FileResponse(load_metadata_file_path("metadata.json"))
