from fastapi import FastAPI
from akipedidos.client import AkiPedidosClient

app = FastAPI(title="Proxy API for Online Service")

client = AkiPedidosClient("https://pedlog.com/")

@app.post("/auth/login")
def login(username: str, password: str):

	session_id = client.session_manager.create_session()
	auth = client.get_auth(session_id)
	if(auth.login(username, password)):

		return {"status": "ok", "session_id": session_id}
	else:
		return{"status": "Failed"}

@app.get("/categories/list")
def get_categories(session_id):
    
    service = client.get_categories(session_id)
    result = service.list()
    return {"status": "ok","value": result}
