from django.apps import AppConfig
from django.core.signals import request_finished
from django.dispatch import receiver

class CrudOrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CRUD_orders'
    
    def ready(self):
        from .utils import get_db_handle
        db_handle, client = get_db_handle()
        self.mongo_db = db_handle
        self.mongo_client = client

        @receiver(request_finished)
        def close_connection(sender, **kwargs):
            self.mongo_client.close()
