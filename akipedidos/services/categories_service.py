from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from ..core.config import settings

class Category:
	
	def __init__(self, session_manager):
		
		self.session_manager = session_manager
		self.panel_url = settings.base_url.rstrip('/') + settings.panel_category_page
		self.register_url = settings.base_url.rstrip('/') + settings.action_get_register_category
		self.edit_url = settings.base_url.rstrip('/') + settings.action_edit_category

	def extract_csrf(self,html):
	    soup = BeautifulSoup(html, "html.parser")
	    tag = soup.find("meta", {"name": "csrf-token"})
	    return tag["content"] if tag else None

	def list(self):
		
		session = self.session_manager.get_session()
		response = session.get(self.panel_url, timeout=10)
		response.raise_for_status()
		soup = BeautifulSoup(response.text, "html.parser")
		spans = soup.find_all("span")
		categories = []
		if spans:
			for span in spans:
				if "id" in span.attrs and span["id"].startswith("strongAdditionalCategory_"):
					categories.append({"id": int(span["id"].replace("strongAdditionalCategory_","")),"name":span.text})

		return categories

	def create(self, name: str, position: int = 0, type_icon: str = "0", icon: str = "fa-tags", icon_name: str = "", days: dict = {'sun':'0','mon':'0','tue':'0','wed':'0','thu':'0','fri':'0','sat':'0'}, icon_file=None):
		
		session = self.session_manager.get_session()
		response = session.get(self.panel_url, timeout=10)
		response.raise_for_status()
		csrf = self.extract_csrf(response.text)
		if not csrf:
			raise RuntimeError('CSRF token not found')

		data = {
			'action': 'registerCategory',
			'name': name,
			'position': str(position),
			'type_icon': type_icon,
			'icon': icon,
			'icon_name': icon_name,
		}

		days = days or {}
		for d in ['sun','mon','tue','wed','thu','fri','sat']:
			data[d] = '1' if days.get(d) else '0'

		files = None
		if icon_file:
			files = {'icon_img': (icon_file.filename, icon_file.file, icon_file.content_type)}

		headers = {'X-CSRF-TOKEN': csrf}
		response = session.post(self.register_url, data=data, files=files, headers=headers, timeout=15)
		response.raise_for_status()
		try:
			return response.json()
		except Exception:
			return {'raw': response.text}

	def edit(self,category_id: int,name: str="",position: int = 0, type_icon: str = "0", icon: str = "", icon_name: str = "", days: dict = {'sun':'0','mon':'0','tue':'0','wed':'0','thu':'0','fri':'0','sat':'0'}, icon_file=None):
		
		session = self.session_manager.get_session()
		response = session.get(self.panel_url, timeout=10)
		response.raise_for_status()
		csrf = self.extract_csrf(response.text)
		if not csrf:
			raise RuntimeError('CSRF token not found')

		data = {
			'action': 'editCategory',
			'id':category_id,
			'name': name,
			'position': str(position),
			'type_icon': type_icon,
			'icon': icon,
			'icon_name': icon_name,
		}

		days = days or {}
		for d in ['sun','mon','tue','wed','thu','fri','sat']:
			data[d] = '1' if days.get(d) else '0'

		files = None
		if icon_file:
			files = {'icon_img': (icon_file.filename, icon_file.file, icon_file.content_type)}

		headers = {'X-CSRF-TOKEN': csrf}
		response = session.post(self.edit_url, data=data, files=files, headers=headers, timeout=15)
		response.raise_for_status()
		try:
			return response.json()
		except Exception:
			return {'raw': response.text}