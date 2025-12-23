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


	def extract_csrf(self, html):
	    soup = BeautifulSoup(html, "html.parser")

	    # Meta tag (authenticated pages)
	    meta = soup.find("meta", {"name": "csrf-token"})
	    print(meta)
	    if meta and meta.get("content"):
	        return meta["content"]

	    # Input fallback (login page)
	    inp = soup.find("input", {"name": "_token"})
	    if inp and inp.get("value"):
	        return inp["value"]

	    return None


	def get_csrf(self,url,timeout = 10):

		response = self.session.get(url, timeout=timeout)
		response.raise_for_status()
		csrf = self.extract_csrf(response.text)

		return csrf

