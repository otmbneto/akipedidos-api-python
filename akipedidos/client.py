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

        # Concrete service interfaces
        self.auth = None
        #self.store = StoreService(self.session)
        self.categories = None
        #self.items = ItemsService(self.session)
        #self.reports = ReportsService(self.session)

    def get_auth(self,session_id):

        return Auth(self.session_manager.get_session(session_id),self.domain)
    def get_categories(self,session_id):
         return CategoryService(self.session_manager.get_session(session_id),self.domain)       

    def get_domain(self):
        return self.domain

    def is_logged(self,session_id) -> bool:
        """Return whether we have a valid authenticated session."""
        return self.session.is_authenticated(session_id)

    def logout(self):
        """Clear cookies and session state."""
        self.session.clear()