from .service import Service
from bs4 import BeautifulSoup
from ..models.hours import Shift,Hours

class ItemsService(Service):

	def __init__(self,session_manager,domain):

		super().__init__(session_manager,domain)

	def _set_service_routes(self,domain):

		self.panel_url = domain + "/panel/company/item"
		self.get_url = domain + "/util/company/getitemsfromcategory"
		self.register_url = domain + "/util/company/registeritem"
		self.edit_url = domain + "/util/company/edititem"
		self.hide_url = domain + "/util/company/setitemhidden"
		self.remove_url = domain + "/util/company/removeitem"


	def list(self,categories: list = []):

		csrf = self.get_csrf(self.panel_url)
		if not csrf:
			return {"items": [], "error": "CSRF token not found"}

		items_list = []
		for category in categories:

			data = {
				"_token": csrf,
				"action": "getItemsFromCategory",
				"page": "myitems",
				"category_id": category["id"],
				"search_item": "-1"
			}

			response = self.session.post(
								self.get_url,
								data=data,
								timeout=10
					)			

			response.raise_for_status()
			data = response.json()
			items = []
			if data.get("success") == "true":
				items = data.get("items", [])
				for item in items:
					item["category_name"] = category["name"]
				items_list += items

		return items_list

	def create(	self,
			    category: str,
			    name: str = "",
			    external_code: str = "",
			    ncm_code: str = "",
			    description: str = "",
			    price: str = "15",
			    price_cost: str = "10",
			    free_shipping: str = "0",
			    is_unavailable_delivery: str = "0",
			    switch_offer: str = "0",
			    price_offer: str = "",
			    item_type: str = "0",
			    price_type: str = "0",
			    amount: str = "-1",
			    unit_measure_type: str = "0",
			    preparation_time: str = "1",
			    serve_people_amount: str = "3",
			    flavor_amount_min: str = "0",
			    flavor_amount: str = "0",
			    days: dict = None,
			    switch_slide: str = "0",
			    slide_items: list = [],
			    hours_json: str = "",
			    img = None,
			):

		csrf = self.get_csrf(self.panel_url)
		if not csrf:
			return {"error": "CSRF token not found"}

		# default days
		if days is None:
			days = {"sun": "1", "mon": "1", "tue": "1", "wed": "1", "thu": "1", "fri": "1", "sat": "1"}

		if len(hours_json) == 0:
			print("hours are empty. creating default")
			hours_json = Hours([Shift([(True, "00:00", "23:59") for _ in range(7)]), Shift(), Shift()])

		data = {
	        "action": "registerItem",
	        "category": category,
	        "name": name,
	        "external_code": external_code,
	        "ncm_code": ncm_code,
	        "description": description,
	        "price": price,
	        "price_cost": price_cost,
	        "free_shipping": free_shipping,
	        "is_unavailable_delivery": is_unavailable_delivery,
	        "switch_offer": switch_offer,
	        "price_offer": price_offer,  # MUST be empty string unless offer enabled
	        "item_type": item_type,
	        "price_type": price_type,
	        "amount": amount,
	        "unit_measure_type": unit_measure_type,
	        "preparation_time": preparation_time,
	        "serve_people_amount": serve_people_amount,
	        "flavor_amount_min": flavor_amount_min,
	        "flavor_amount": flavor_amount,
	        "switch_slide": switch_slide,
	        "hours": str(hours_json),
	    }

		days = days or {}
		for d in ['sun','mon','tue','wed','thu','fri','sat']:
			data[d] = '1' if days.get(d) else '0'

		files = None
		if img:
			files = {
				"img": (
					img.filename,
					img.file,
					img.content_type or "application/octet-stream"
				)
			}

		# Insert slide items
		if switch_slide == "1":
			
			if files is None:
				files = {}

			for i, slide in enumerate(slide_items):
				files[f"slide_item_{i}"] = (
											slide.filename,
											slide.file,
											slide.content_type or "application/octet-stream"
										  )


		headers = {"X-CSRF-TOKEN": csrf}
		response = self.session.post(self.register_url, data=data, files=files,headers=headers)
		try:
			resp.raise_for_status()
			return resp.json()
		except:
			return {"raw": response.text}

	def edit(self,
				id:int,
				category: str,
				name: str = "",
				external_code: str = "",
				ncm_code: str = "",
				description: str = "",
				price: str = "15",
				price_cost: str = "10",
				free_shipping: str = "0",
				is_unavailable_delivery: str = "0",
				switch_offer: str = "0",
				price_offer: str = "",
				item_type: str = "0",
				price_type: str = "0",
				amount: str = "-1",
				unit_measure_type: str = "0",
				preparation_time: str = "1",
				serve_people_amount: str = "3",
				flavor_amount_min: str = "0",
				flavor_amount: str = "0",
				days: dict = None,
				switch_slide: str = "0",
				slide_items: list = [],
				hours_json: str = "",
				img = None,
			):

		csrf = self.get_csrf(self.panel_url)
		if not csrf:
			return {"error": "CSRF token not found"}

		# default days
		if days is None:
			days = {"sun": "1", "mon": "1", "tue": "1", "wed": "1", "thu": "1", "fri": "1", "sat": "1"}

		data = {
			"action": "editItem",
			"id": id,
			"category": category,
			"name": name,
			"external_code": external_code,
			"ncm_code": ncm_code,
			"description": description,
			"price": price,
			"price_cost": price_cost,
			"free_shipping": free_shipping,
			"is_unavailable_delivery": is_unavailable_delivery,
			"switch_offer": switch_offer,
			"price_offer": price_offer,
			"item_type": item_type,
			"price_type": price_type,
			"amount": amount,
			"unit_measure_type": unit_measure_type,
			"preparation_time": preparation_time,
			"serve_people_amount": serve_people_amount,
			"flavor_amount_min": flavor_amount_min,
			"flavor_amount": flavor_amount,
			"switch_slide": switch_slide,
			"hours": hours_json,
		}

		days = days or {}
		for d in ['sun','mon','tue','wed','thu','fri','sat']:
			data[d] = '1' if days.get(d) else '0'

		files = None
		if img:
			files = {
				"img": (
				img.filename,
				img.file,
				img.content_type or "application/octet-stream"
				)
			}

		# Insert slide items
		if switch_slide == "1":

			if files is None:
				files = {}

				for i, slide in enumerate(slide_items):
					files[f"slide_item_{i}"] = (
								slide.filename,
								slide.file,
								slide.content_type or "application/octet-stream"
							  )

		headers = {"X-CSRF-TOKEN": csrf}
		response = self.session.post(self.edit_url, data=data, headers=headers)
		try:
			resp.raise_for_status()
			return resp.json()
		except:
			return {"raw": response.text}


	def delete(self,item_id: int):

		csrf = self.get_csrf(self.panel_url)
		if not csrf:
			raise RuntimeError('CSRF token not found')
	    
		data = {
			'action': 'removeItem',
			'id': item_id,
			'_token': csrf,
		}

		response = self.session.post(self.remove_url, data=data, timeout=15)
		response.raise_for_status()
		try:
			return response.json()
		except Exception:
			return {'raw': response.text}

	def hide(self,item_id:int,hidden:bool):

		csrf = self.get_csrf(self.panel_url)
		if not csrf:
			raise RuntimeError('CSRF token not found')

		data = {
			'action': "setItemHidden",
			'id': item_id,
			'_token': csrf,
			'type': "true" if hidden else "false",
		}

		response = self.session.post(self.hide_url, data=data, timeout=15)
		#response.raise_for_status()
		try:
			return response.json()
		except Exception:
			return {'raw': response.text}