from .service import Service
from bs4 import BeautifulSoup

class ReportsService(Service):

    def __init__(self,session_manager):

        super().__init__(session_manager) 

    def _set_service_routes(self,domain):

        self.panel_url = domain.rstrip('/') + "/panel/company/report"
        self.order_url =  domain.rstrip('/') + "/util/company/getordersreport"

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