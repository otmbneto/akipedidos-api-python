from .service import Service
from bs4 import BeautifulSoup

class Auth(Service):
	
	def __init__(self, session,domain):

		super().__init__(session,domain) 

	def _set_service_routes(self,domain):

		self.login_url = domain + "/panel/company"
		self.login_adm = domain + "/panel/admin/login"

	def login(self, email: str, password: str, selectUserType = "0"):

		login_page = self.login_adm if str(selectUserType) == "4" else self.login_url
		token = self.get_csrf(login_page)
		if not token:
			raise RuntimeError('CSRF token not found')

		data = {
			"email": email,
			"password": password,
			"_token": token,
			"selectUserType": selectUserType,
		}

		post = self.session.post(
			login_page,
			data=data,
			allow_redirects=True,
			timeout=15,
		)

		post.raise_for_status()

		return post.text
