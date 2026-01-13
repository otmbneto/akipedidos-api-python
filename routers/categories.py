import json
from fastapi import APIRouter, Depends, HTTPException,Form,UploadFile,File
from pydantic import BaseModel
from akipedidos.client import AkiPedidosClient
from dependencies import get_client,get_session_id

router = APIRouter(prefix="/categories")

@router.get("/list", tags=["Categories"])
def list_categories(
    client: AkiPedidosClient = Depends(get_client),
    session_id: str = Depends(get_session_id),
):
    categories = client.get_all_categories(session_id)
    return {"status": "ok", "categories": categories}

@router.post("/create", tags=["Categories"])
def create_category(
    payload: str = Form(...),
    img: UploadFile | None = File(None),
    client: AkiPedidosClient = Depends(get_client),
    session_id: str = Depends(get_session_id),
):

    data = json.loads(payload)
    if img is not None:
        data["img"] = img

    result = client.create_category(session_id,data)
    return {"status": "ok", "result": result}

@router.post("/edit", tags=["Categories"])
def edit_category(
    payload: dict,
    client: AkiPedidosClient = Depends(get_client),
    session_id: str = Depends(get_session_id),
):
    result = client.edit_category(session_id,payload)
    return {"status": "ok", "result": result}

@router.post("/delete", tags=["Categories"])
def delete_category(
    category_id: str,
    client: AkiPedidosClient = Depends(get_client),
    session_id: str = Depends(get_session_id),
):
    result = client.delete_category(session_id,category_id)
    return {"status": "ok", "result": result}

@router.post("/hide", tags=["Categories"])
def hide_category(
    category_id: str,
    client: AkiPedidosClient = Depends(get_client),
    session_id: str = Depends(get_session_id),
    hidden: bool = Form(False),
):
    result = client.hide_category(session_id,category_id,hidden)
    return {"status": "ok", "result": result}