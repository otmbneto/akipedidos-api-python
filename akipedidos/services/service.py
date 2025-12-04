from bs4 import BeautifulSoup

class Service:
	
	def __init__(self,session,domain):
		
		self.session = session
		self._set_service_routes(domain)

	def _set_service_routes(domain):

		return

	def set_session(self,session,domain):

		self.session = session
		self._set_service_routes(domain)

	def extract_csrf(self,html):
		soup = BeautifulSoup(html, "html.parser")
		tag = soup.find("meta", {"name": "csrf-token"})
		return tag["content"] if tag else None

	def get_csrf(self,url,timeout = 10):

		response = self.session.get(url, timeout=timeout)
		response.raise_for_status()
		csrf = self.extract_csrf(response.text)

		return csrf

