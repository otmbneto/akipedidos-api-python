from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from akipedidos.client import AkiPedidosClient
from dependencies import *

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(
          payload:dict,
          client: AkiPedidosClient = Depends(get_client)
):
    """Login and return a session_id."""
    auth,session_id = client.get_auth()
    result = auth.login(payload["email"], payload["password"])

    if session_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"success": result, "session_id": session_id if result else None}


@router.post("/logout")
def logout(
    client: AkiPedidosClient = Depends(get_client),
    session_id: str = Depends(get_session_id),
):
    """Logout and destroy the session."""
    result = client.logout(session_id = session_id)
    return {"result": result}