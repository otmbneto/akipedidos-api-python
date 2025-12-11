import requests
from uuid import uuid4
from bs4 import BeautifulSoup

class SessionManager:
    
	def __init__(self,domain):

		self.domain = domain
		self.sessions = {}

	def create_session(self):

		new_id = str(uuid4())
		new_session = requests.Session()
		self.sessions[new_id] = new_session

		return new_id

	def get_session(self,session_id):
		print("\n--- SESSION DEBUG ---")
		print("Current sessions:", self.sessions.keys())
		print("Requested session:", session_id)
		print("---------------------\n")
		return self.sessions[session_id] if session_id in self.sessions.keys() else None

	def delete_session(self,session_id):
		if session_id in self.sessions.keys():
			del self.sessions[session_id]

	def get_domain(self):
		return self.domain

	def is_authenticated(self,session_id):

		session = self.get_session(session_id)
		if session is None:
			return {"valid":False,
					"reason": "Session id not valid"}

		PROTECTED_URL = self.domain + "/panel/company/report"
		try:
			response = session.get(PROTECTED_URL, timeout=10)
		except Exception:
			return {"valid": False, "reason": "Request failed"}

		soup = BeautifulSoup(response.text, "html.parser")
		has_email = soup.find("input", {"name": "email"})
		has_password = soup.find("input", {"name": "password"})
		has_token = soup.find("input", {"name": "_token"})

		if has_email and has_password and has_token:
			return {
				"valid": False,
				"reason": "Login form detected (user is not authenticated)"
			}

		# Otherwise, we are logged in
		return {
			"valid": True,
			"details": {
				"url": response.url,
				"title": soup.title.string if soup.title else "No title"
			}
		}