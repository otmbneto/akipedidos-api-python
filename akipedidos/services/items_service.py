from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from ..core.config import settings

class ItemsService:

	def __init__(self,session_manager):

		self.session_manager = session_manager
		self.panel_url = settings.base_url.rstrip('/') + settings.panel_item_page
		self.get_url = settings.base_url.rstrip('/') + settings.action_get_items_from_category
		self.register_url = settings.base_url.rstrip('/') + settings.action_register_item
		self.edit_url = settings.base_url.rstrip('/') + settings.action_edit_item
		self.hide_url = settings.base_url.rstrip('/') + settings.action_hide_item

	def extract_csrf(self,html):
	    soup = BeautifulSoup(html, "html.parser")
	    tag = soup.find("meta", {"name": "csrf-token"})
	    return tag["content"] if tag else None

	def list(self,categories: list = []):

		session = self.session_manager.get_session()

		# Load the main Items page to fetch the CSRF token
		response = session.get(self.panel_url, timeout=10)
		response.raise_for_status()
		csrf = self.extract_csrf(response.text)
		if not csrf:
			return {"items": [], "error": "CSRF token not found"}

		data = {
			"_token": csrf,
			"action": "getItemsFromCategory",
			"page": "myitems",
			"search_item": "-1"
		}

		for category in categories:

			data["category_id"] = category["id"]

		response = session.post(
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

		return items

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
			    slide_item: list = None,
			    hours_json: str = "",
			):

	    session = self.session_manager.get_session()
	    response = session.get(self.panel_url, timeout=10)
	    response.raise_for_status()
	    csrf = self.extract_csrf(response.text)
	    if not csrf:
	        return {"error": "CSRF token not found"}


	    # default days
	    if days is None:
	        days = {"sun": "1", "mon": "1", "tue": "1", "wed": "1", "thu": "1", "fri": "1", "sat": "1"}


	    # base payload EXACTLY like Chrome sends
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
	        "hours": hours_json,
	    }

	    days = days or {}
	    for d in ['sun','mon','tue','wed','thu','fri','sat']:
	        data[d] = '1' if days.get(d) else '0'

	    # Insert slide items
	    if slide_item:
	        for i, slide in enumerate(slide_item):
	            data[f"slide_item_{i}"] = slide
	    
	    headers = {"X-CSRF-TOKEN": csrf}
	    response = session.post(self.register_url, data=data, headers=headers)
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
			    slide_item: list = None,
			    hours_json: str = "",
			):

	    session = self.session_manager.get_session()
	    response = session.get(self.panel_url, timeout=10)
	    response.raise_for_status()
	    csrf = self.extract_csrf(response.text)
	    if not csrf:
	        return {"error": "CSRF token not found"}

	    # default days
	    if days is None:
	        days = {"sun": "1", "mon": "1", "tue": "1", "wed": "1", "thu": "1", "fri": "1", "sat": "1"}


	    # base payload EXACTLY like Chrome sends
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
	        "hours": hours_json,
	    }

	    days = days or {}
	    for d in ['sun','mon','tue','wed','thu','fri','sat']:
	        data[d] = '1' if days.get(d) else '0'

	    # Insert slide items
	    if slide_item:
	        for i, slide in enumerate(slide_item):
	            data[f"slide_item_{i}"] = slide
	    
	    headers = {"X-CSRF-TOKEN": csrf}
	    response = session.post(self.edit_url, data=data, headers=headers)
	    print(response)
	    try:
	        print("RAW TEXT: " + str(response.text))
	        resp.raise_for_status()
	        return resp.json()
	    except:
	        return {"raw": response.text}

	def hide(self,item_id:int,hidden):

		session = self.session_manager.get_session()
		response = session.get(self.panel_url, timeout=10)
		response.raise_for_status()
		csrf = self.extract_csrf(response.text)
		if not csrf:
			raise RuntimeError('CSRF token not found')

		data = {
			'action': "setItemHidden",
			'id': item_id,
			'_token': csrf,
			'type': "true" if hidden else "false",
		}

		response = session.post(self.hide_url, data=data, timeout=15)
		#response.raise_for_status()
		try:
			return response.json()
		except Exception:
			return {'raw': response.text}

		return
