from .service import Service
from bs4 import BeautifulSoup

class ReportsService(Service):

    def __init__(self,session_manager):

        super().__init__(session_manager) 

    def _set_service_routes(self,domain):

        self.panel_url = domain.rstrip('/') + "/panel/company/report"
        self.order_url =  domain.rstrip('/') + "/util/company/getordersreport"
        self.item_url = domain.rstrip('/') + "/util/company/getitemsreport"

    def get_orders_report(self,date_initial,date_final):

        csrf = self.get_csrf(self.panel_url)
        if not csrf:
            return {"error": "CSRF token not found"}

        data = {
                "action":'getOrdersReport',
                "date_initial": date_initial, 
                "date_final": date_final,
                "_token": csrf,
        }

        response = self.session.post(self.order_url, data=data, timeout=15)
        response.raise_for_status()
        try:
            return response.json()
        except Exception:
            return {'raw': response.text}


    def get_item_report(self,date_initial,date_final,show_all_items = False):

        csrf = self.get_csrf(self.panel_url)
        if not csrf:
            return {"error": "CSRF token not found"}

        data = {
                "action":'getItemsReport',
                "date_initial": date_initial if not show_all_items else "", 
                "date_final": date_final if not show_all_items else "",
                "show_all_items": "1" if show_all_items else "0",
                "_token": csrf,
        }

        response = self.session.post(self.item_url, data=data, timeout=15)
        response.raise_for_status()
        try:
            return response.json()
        except Exception:
            return {'raw': response.text}