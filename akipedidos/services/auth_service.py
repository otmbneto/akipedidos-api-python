from typing import Optional
from bs4 import BeautifulSoup
from ..core.config import settings

class Auth:
	
	def __init__(self, session_manager):

		self.session_manager = session_manager

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

	def login(self, username: str, password: str) -> Optional[bool]:
		
		LOGIN_PAGE_URL = settings.base_url + settings.login_path
		session = self.session_manager.get_session()
		response = session.get(LOGIN_PAGE_URL, timeout=15)
		response.raise_for_status()

		fields = self._extract_form_fields(response.text)

		print(fields)
		# overwrite credentials
		fields['email'] = username
		fields['password'] = password

		if "is_employee" in fields:
			del fields["is_employee"]

		soup = BeautifulSoup(response.text, "html.parser")
		form = soup.find("form")
		action = LOGIN_PAGE_URL

		if form and form.get('action'):
			act = form.get('action')
			if act.startswith('/'):
				action = settings.base_url.rstrip('/') + act
			elif act.startswith('http'):
				action = act
			else:
				action = LOGIN_PAGE_URL.rstrip('/') + '/' + act.lstrip('/')

		post = session.post(action, data=fields, allow_redirects=True, timeout=15)
		post.raise_for_status()
		# simple heuristic: if the response contains the login form again, fail
		if 'name="email"' in post.text and 'name="password"' in post.text:
			return False

		return True