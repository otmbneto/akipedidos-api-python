from .service import Service
from bs4 import BeautifulSoup

class CategoryService(Service):
	
	def __init__(self, session,domain):
		
		super().__init__(session,domain) 

	def _set_service_routes(self,domain):

		self.panel_url = domain + "/panel/company/category"
		self.register_url = domain + "/util/company/registercategory"
		self.edit_url = domain + "/util/company/editcategory"
		self.remove_url = domain + "/util/company/removecategory"
		self.hide_url = domain + "/util/company/setcategoryhidden"

	def list(self):
		
		categories = []
		if self.session is None:
			print("ERROR: Session not found!")
			return categories

		response = self.session.get(self.panel_url, timeout=10)
		response.raise_for_status()
		soup = BeautifulSoup(response.text, "html.parser")
		spans = soup.find_all("span")
		if spans:
			for span in spans:
				if "id" in span.attrs and span["id"].startswith("strongAdditionalCategory_"):
					cat_data = {"id": int(span["id"].replace("strongAdditionalCategory_",""))}
					
					for attr in ["name","position","type_icon","icon","icon_name","icon_img"]:
						match = soup.find("input",{"id": attr + "_" + str(cat_data["id"])})
						if match:
							cat_data[attr] = match.get("value")

					cat_data["days"] = {}
					
					for attr in ["sun","mon","tue","wed","thu","fri","sat"]:
						match = soup.find("input",{"id": attr + "_" + str(cat_data["id"])})
						if match:
							cat_data["days"][attr] = match.get("value")

					categories.append(cat_data)

		return categories

	def create(self, name: str, position: int = 0, type_icon: str = "0", icon: str = "fa-tags", icon_name: str = "", days: dict = {'sun':'0','mon':'0','tue':'0','wed':'0','thu':'0','fri':'0','sat':'0'}, icon_file=None):
		
		if self.session is None:
			print("ERROR: Session not found!")
			return {'raw': "session error"}

		csrf = self.get_csrf(self.panel_url)
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
		response = self.session.post(self.register_url, data=data, files=files, headers=headers, timeout=15)
		response.raise_for_status()
		try:
			return response.json()
		except Exception:
			return {'raw': response.text}

	def edit(self,category_id: int,name: str="",position: int = 0, type_icon: str = "0", icon: str = "", icon_name: str = "", days: dict = {'sun':'0','mon':'0','tue':'0','wed':'0','thu':'0','fri':'0','sat':'0'}, icon_file=None):
		
		if self.session is None:
			print("ERROR: Session not found!")
			return {'raw': "session error"}
			
		csrf = self.get_csrf(self.panel_url)
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
		response = self.session.post(self.edit_url, data=data, files=files, headers=headers, timeout=15)
		response.raise_for_status()
		try:
			return response.json()
		except Exception:
			return {'raw': response.text}

	def delete(self,category_id: int):

		csrf = self.get_csrf(self.panel_url)
		if not csrf:
			raise RuntimeError('CSRF token not found')
	    
		data = {
			'action': 'removeCategory',
			'id': category_id,
			'_token': csrf,
		}

		response = self.session.post(self.remove_url, data=data, timeout=15)
		response.raise_for_status()
		try:
			return response.json()
		except Exception:
			return {'raw': response.text}

	def hide(self,category_id: int,hidden: bool):
	
		csrf = self.get_csrf(self.panel_url)
		if not csrf:
			raise RuntimeError('CSRF token not found')

		data = {
			'action': 'setCategoryHidden',
			'id': category_id,
			'_token': csrf,
			'hidden': "1" if hidden else "0",
		}

		response = self.session.post(self.hide_url, data=data, timeout=15)
		try:
			return response.json()
		except Exception as e:
			return {'exception':e,'raw': response.text}

