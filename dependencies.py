from fastapi import Header, HTTPException
from akipedidos.client import AkiPedidosClient

client = AkiPedidosClient("https://pedlog.com")

def get_client():
    """
    Returns an AkiPedidos client instance.
    You can later extend this to support multi-domain if needed.
    """
    return client

def get_session_id(x_session_id: str = Header(..., alias="X-Session-ID")):
    """
    Required header for authenticated calls.
    Example request header:
        X-Session-ID: abc123
    """
    if not x_session_id:
        raise HTTPException(status_code=400, detail="X-Session-ID header missing")
    return x_session_id
