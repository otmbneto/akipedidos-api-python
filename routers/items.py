from fastapi import APIRouter, Depends, HTTPException,Form
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
    payload: dict,
    client: AkiPedidosClient = Depends(get_client),
    session_id: str = Depends(get_session_id),
):
    result = client.create_item(session_id,payload)
    return {"status": "ok", "result": result}

@router.post("/edit", tags=["Items"])
def edit_item(
    payload: dict,
    client: AkiPedidosClient = Depends(get_client),
    session_id: str = Depends(get_session_id),
):
    result = client.edit_item(session_id,payload)
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