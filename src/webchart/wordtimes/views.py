from django.shortcuts import render
from django.http import HttpResponse
from .resource import Wordresource
from tablib import Dataset

# Create your views here.

def export(request):
    person_resource = Wordresource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    return response

def simple_upload(request):
    if request.method == 'POST':
        person_resource = Wordresource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'core/simple_upload.html')

def home(request):
    return render(request, 'home.html')