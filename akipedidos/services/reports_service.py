from .service import Service
from bs4 import BeautifulSoup

class ReportsService(Service):

    def __init__(self,session_manager,domain):

        super().__init__(session_manager,domain) 

    def _set_service_routes(self,domain):

        self.panel_url = domain.rstrip('/') + "/panel/company/report"
        self.order_url =  domain.rstrip('/') + "/util/company/getordersreport"
        self.item_url = domain.rstrip('/') + "/util/company/getitemsreport"
        self.additional_url = domain.rstrip('/') + "/util/company/getadditionalsreport"
        self.crashDrawer_url = domain.rstrip('/') + "/util/company/getcashdrawerreport"
        self.deliveryMan_url = domain.rstrip('/') + "/util/company/getdeliverymansreport"

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


    def get_additional_report(self,date_initial,date_final,show_all_additionals = False):

        csrf = self.get_csrf(self.panel_url)
        if not csrf:
            return {"error": "CSRF token not found"}

        data = {
                "action":'getAdditionalsReport',
                "date_initial": date_initial if not show_all_additionals else "", 
                "date_final": date_final if not show_all_additionals else "",
                "show_all_additionals": "1" if show_all_additionals else "0",
                "_token": csrf,
        }

        response = self.session.post(self.additional_url, data=data, timeout=15)
        response.raise_for_status()
        try:
            return response.json()
        except Exception:
            return {'raw': response.text}

    def get_cash_drawer_report(self,date_initial,date_final):

        csrf = self.get_csrf(self.panel_url)
        if not csrf:
            return {"error": "CSRF token not found"}

        data = {
                "action":'getCashDrawerReport',
                "date_initial": date_initial, 
                "date_final": date_final,
                "_token": csrf,
        }

        response = self.session.post(self.crashDrawer_url, data=data, timeout=15)
        response.raise_for_status()
        try:
            return response.json()
        except Exception:
            return {'raw': response.text}

    def get_deliveryman_report(self,date_initial,date_final):

        csrf = self.get_csrf(self.panel_url)
        if not csrf:
            return {"error": "CSRF token not found"}

        data = {
                "action":'getDeliverymansReport',
                "date_initial": date_initial, 
                "date_final": date_final,
                "_token": csrf,
        }

        response = self.session.post(self.deliveryMan_url, data=data, timeout=15)
        response.raise_for_status()
        try:
            return response.json()
        except Exception:
            return {'raw': response.text}

