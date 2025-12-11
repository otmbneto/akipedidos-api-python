from .session.manager import SessionManager
from .services.auth_service import Auth
from .services.categories_service import CategoryService
from .services.items_service import ItemsService
from .services.reports_service import ReportsService
from .services.store_service import StoreService

class AkiPedidosClient:
    """
    Main entry point for interacting with the AkiPedidos API.
    """

    def __init__(self,domain):
        # Session manager handles:
        # - cookies
        # - CSRF tokens
        # - logged state
        # - base headers

        self.domain = domain
        self.session_manager = SessionManager(domain)

    def get_auth(self,session_id = None):

        #create a new session
        if session_id is None:
            session_id = self.session_manager.create_session()
        return Auth(self.session_manager.get_session(session_id),self.domain),session_id

    #----------------------------------CATAGORIES------------------------------------------
    def create_category(self,session_id,payload):

        print(self.session_manager.sessions)
        service = CategoryService(self.session_manager.get_session(session_id),self.domain)
        return service.create(**payload)

    def edit_category(self,session_id,payload):

        service = CategoryService(self.session_manager.get_session(session_id),self.domain)
        return service.edit(**payload)

    def delete_category(self,session_id,category_id):

        service = CategoryService(self.session_manager.get_session(session_id),self.domain)
        return service.delete(category_id)

    def hide_category(self,session_id,category_id,hidden):

        service = CategoryService(self.session_manager.get_session(session_id),self.domain)
        return service.hide(category_id,hidden)    

    def get_all_categories(self,session_id):
        
        service = CategoryService(self.session_manager.get_session(session_id),self.domain)
        return service.list()

    #---------------------------------------------------------------------------------------
    
    #-------------------------------------ITEMS--------------------------------------------
    def create_item(self,session_id,payload):

        service = ItemsService(self.session_manager.get_session(session_id),self.domain)
        return service.create(**payload)

    def edit_item(self,session_id,payload):

        service = ItemsService(self.session_manager.get_session(session_id),self.domain)
        return service.edit(**payload)

    def delete_item(self,session_id,item_id):

        service = ItemsService(self.session_manager.get_session(session_id),self.domain)
        return service.delete(item_id)

    def hide_item(self,session_id,item_id,hidden):

        service = ItemsService(self.session_manager.get_session(session_id),self.domain)
        return service.hide(item_id,hidden)    

    def get_all_items(self,session_id):
        
        categories = self.get_all_categories(session_id)
        service = ItemsService(self.session_manager.get_session(session_id),self.domain)
        return service.list(categories = categories)
    #---------------------------------------------------------------------------------------

    #-------------------------------------REPORT--------------------------------------------

    def get_items_reports(self,session_id,start_date,end_date,show_all_items = False):

        service = ReportsService(self.session_manager.get_session(session_id),self.domain)
        return service.get_item_reports(start_date,end_date,show_all_items = show_all_items)

    def get_orders_report(self,session_id,date_initial,date_final):

        service = ReportsService(self.session_manager.get_session(session_id),self.domain)
        return service.get_orders_reports(start_date,end_date)
    
    def get_additional_report(self,session_id,date_initial,date_final,show_all_additionals = False):

        service = ReportsService(self.session_manager.get_session(session_id),self.domain)
        return service.get_additional_report(start_date,end_date,show_all_additionals = show_all_additionals)

    def get_cash_drawer_report(self,session_id,date_initial,date_final):

        service = ReportsService(self.session_manager.get_session(session_id),self.domain)
        return service.get_cash_drawer_report(start_date,end_date)

    def get_deliveryman_report(self,session_id,date_initial,date_final):

        service = ReportsService(self.session_manager.get_session(session_id),self.domain)
        return service.get_deliveryman_report(start_date,end_date)

    #---------------------------------------------------------------------------------------

    #-------------------------------------STORE---------------------------------------------

    def edit_store(self,session_id,payload):
        service = StoreService(self.session_manager.get_session(session_id),self.domain)
        return service.edit(**payload)

    #---------------------------------------------------------------------------------------

    def get_domain(self):
        return self.domain

    def is_logged(self,session_id) -> bool:
        """Return whether we have a valid authenticated session."""
        return self.session_manager.is_authenticated(session_id)

    def logout(self,session_id):
        self.session_manager.delete_session(session_id)