import json
from fastapi import APIRouter, Depends, HTTPException,Form,UploadFile,File
from pydantic import BaseModel
from akipedidos.client import AkiPedidosClient
from dependencies import get_client,get_session_id

router = APIRouter(prefix="/items")

@router.get("/list", tags=["Items"])
def list_items(
    client: AkiPedidosClient = Depends(get_client),
    session_id: str = Depends(get_session_id),
):
    items = client.get_all_items(session_id)
    return {"status": "ok", "items": items}

@router.post("/create", tags=["Items"])
def create_item(
    payload: str = Form(...),
    img: UploadFile | None = File(None),
    slide_item_0: UploadFile | None = File(None),
    slide_item_1: UploadFile | None = File(None),
    slide_item_2: UploadFile | None = File(None),
    slide_item_3: UploadFile | None = File(None),
    slide_item_4: UploadFile | None = File(None),
    client: AkiPedidosClient = Depends(get_client),
    session_id: str = Depends(get_session_id),
):

    data = json.loads(payload)
    if img is not None:
        data["img"] = img

    temp = [slide_item_0,slide_item_1,slide_item_2,slide_item_3,slide_item_4]
    data["slide_items"] = []
    for t in temp:
        if t is None:
            break
        data["slide_items"].append(t)
        data["switch_slide"] = "1"


    result = client.create_item(session_id,data)
    return {"status": "ok", "result": result}

@router.post("/edit", tags=["Items"])
def edit_item(
    payload: str = Form(...),
    img: UploadFile | None = File(None),
    slide_item_0: UploadFile | None = File(None),
    slide_item_1: UploadFile | None = File(None),
    slide_item_2: UploadFile | None = File(None),
    slide_item_3: UploadFile | None = File(None),
    slide_item_4: UploadFile | None = File(None),
    client: AkiPedidosClient = Depends(get_client),
    session_id: str = Depends(get_session_id),
):

    data = json.loads(payload)
    if img is not None:
        data["img"] = img

    temp = [slide_item_0,slide_item_1,slide_item_2,slide_item_3,slide_item_4]
    data["slide_items"] = []
    for t in temp:
        if t is None:
            break
        data["slide_items"].append(t)
        data["switch_slide"] = "1"

    result = client.edit_item(session_id,data)
    return {"status": "ok", "result": result}

@router.post("/delete", tags=["Items"])
def delete_item(
    payload: dict,
    client: AkiPedidosClient = Depends(get_client),
    session_id: str = Depends(get_session_id),
):
    result = client.delete_item(session_id,payload["item_id"])
    return {"status": "ok", "result": result}

@router.post("/hide", tags=["Items"])
def hide_item(
    payload: dict,
    client: AkiPedidosClient = Depends(get_client),
    session_id: str = Depends(get_session_id),
):
    result = client.hide_item(session_id,payload["item_id"],payload["hidden"])
    return {"status": "ok", "result": result}