from django.contrib import admin
from .models import WORD
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(WORD)
class Word(ImportExportModelAdmin):
    pass
