from import_export import resources
from .models import WORD

class Wordresource(resources.ModelResource):
    class Mate:
        model = WORD