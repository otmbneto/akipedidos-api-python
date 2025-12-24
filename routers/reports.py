from fastapi import APIRouter, Depends, HTTPException,Form
from pydantic import BaseModel
from akipedidos.client import AkiPedidosClient
from dependencies import get_client,get_session_id

router = APIRouter(prefix="/reports")
@router.post("/orders", tags=["Reports"])
def get_orders_report(payload: dict,
                    client: AkiPedidosClient = Depends(get_client),
                    session_id: str = Depends(get_session_id)):
    
    return client.get_orders_report(session_id,payload["start_date"],payload["end_date"])


@router.post("/items", tags=["Reports"])
def get_items_report(payload: dict,
                    client: AkiPedidosClient = Depends(get_client),
                    session_id: str = Depends(get_session_id)):
    return client.get_items_report(session_id,payload["start_date"],payload["end_date"],show_all_items = payload["show_all_items"])

@router.post("/additionals", tags=["Reports"])
def get_additionals_report(payload: dict,
                           client: AkiPedidosClient = Depends(get_client),
                           session_id: str = Depends(get_session_id)):
    return client.get_additionals_report(session_id,payload["start_date"],payload["end_date"],show_all_additionals = payload["show_all_additionals"])

@router.post("/cashdrawer", tags=["Reports"])
def get_cash_drawer_report(payload: dict,
                            client: AkiPedidosClient = Depends(get_client),
                            session_id: str = Depends(get_session_id)):
    return client.get_cash_drawer_report(session_id,payload["start_date"],payload["end_date"])

@router.post("/deliverymen", tags=["Reports"])
def get_deliverymen_report(payload: dict,
                        client: AkiPedidosClient = Depends(get_client),
                        session_id: str = Depends(get_session_id)):

   return client.get_deliverymen_report(session_id,payload["start_date"],payload["end_date"])

