from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from ..core.config import settings

class ItemsService:

	def __init__(self,session_manager):

		self.session_manager = session_manager
		self.panel_url = settings.base_url.rstrip('/') + settings.panel_item_page
		self.get_url = settings.base_url.rstrip('/') + settings.action_get_items_from_category

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