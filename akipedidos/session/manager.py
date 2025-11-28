import requests
from uuid import uuid4
from bs4 import BeautifulSoup

class SessionManager:
    
	def __init__(self,domain):

		self.domain = domain
		self.session_id = str(uuid4())
		self.session = requests.Session()

	def get_session(self):
		return self.session

	def get_session_id(self):
		return session_id

	def clear(self):
		self.session.cookies.clear()

	def get_domain(self):
		return self.domain

	def is_authenticated(self) -> dict:

		PROTECTED_URL = self.domain + "/panel/company/report"
		try:
			response = self.session.get(PROTECTED_URL, timeout=10)
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
				"url": resp.url,
				"title": soup.title.string if soup.title else "No title"
			}
		}