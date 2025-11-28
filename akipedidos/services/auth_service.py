from typing import Optional
from bs4 import BeautifulSoup

class Auth:
	
	def __init__(self, session_manager):

		self.session = session_manager.get_session()
		self._set_service_routes(session_manager.get_domain())

	def _set_service_routes(self,domain):

		self.login_url = domain + "/panel/company"

	def _extract_form_fields(self,html: str) -> dict:
	    
	    soup = BeautifulSoup(html, "html.parser")
	    form = soup.find("form")
	    fields = {}
	    if not form:
	        return fields

	    # hidden and visible inputs
	    for inp in form.find_all("input"):
	        name = inp.get("name")
	        if not name:
	            continue
	        itype = (inp.get("type") or "").lower()
	        if itype == "checkbox":
	            if inp.has_attr("checked") or inp.get("value"):
	                fields[name] = inp.get("value", "1")
	        else:
	            fields[name] = inp.get("value", "")

	    return fields

	def login(self,email: str, password: str) -> Optional[bool]:
		
		response = self.session.get(self.login_url, timeout=15)
		response.raise_for_status()

		fields = self._extract_form_fields(response.text)

		fields['email'] = email
		fields['password'] = password

		if "is_employee" in fields:
			del fields["is_employee"]

		soup = BeautifulSoup(response.text, "html.parser")
		form = soup.find("form")
		action = self.login_url

		if form and form.get('action'):
			act = form.get('action')
			if act.startswith('/'):
				action = settings.base_url.rstrip('/') + act
			elif act.startswith('http'):
				action = act
			else:
				action = self.login_url.rstrip('/') + '/' + act.lstrip('/')

		post = self.session.post(action, data=fields, allow_redirects=True, timeout=15)
		post.raise_for_status()

		if 'name="email"' in post.text and 'name="password"' in post.text:
			return False

		return True