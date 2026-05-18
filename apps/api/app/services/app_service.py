# apps/api/app/services/app_service.py

class AppService:
    """
    Service layer for core monorepo operations.
    """
    def __init__(self):
        pass

    def get_welcome_message(self):
        return {
            "title": "Welcome to the Monorepo",
            "description": "This is the initial scaffold for the fullstack monorepo topology."
        }
