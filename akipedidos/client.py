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
        self.session = SessionManager(domain)

        # Concrete service interfaces
        self.auth = Auth(self.session)
        self.store = StoreService(self.session)
        self.categories = CategoryService(self.session)
        self.items = ItemsService(self.session)
        self.reports = ReportsService(self.session)

    def is_logged(self) -> bool:
        """Return whether we have a valid authenticated session."""
        return self.session.is_authenticated()

    def logout(self):
        """Clear cookies and session state."""
        self.session.clear()