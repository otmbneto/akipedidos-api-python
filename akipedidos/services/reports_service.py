from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from ..core.config import settings

class ReportsService:

    def __init__(self,session_manager):

        self.session_manager = session_manager
        self.panel_url = settings.base_url.rstrip('/') + "/panel/company/report"
        self.order_url =  settings.base_url.rstrip('/') + "/util/company/getordersreport"

    def extract_csrf(self,html):
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.find("meta", {"name": "csrf-token"})
        return tag["content"] if tag else None

    def get_orders_report(self,date_initial,date_final):

        session = self.session_manager.get_session()
        response = session.get(self.panel_url, timeout=10)
        response.raise_for_status()
        csrf = self.extract_csrf(response.text)
        if not csrf:
            return {"error": "CSRF token not found"}

        data = {
                "action":'getOrdersReport',
                "date_initial": date_initial, 
                "date_final": date_final,
                "_token": csrf,
        }

        response = session.post(self.order_url, data=data, timeout=15)
        response.raise_for_status()
        try:
            return response.json()
        except Exception:
            return {'raw': response.text}