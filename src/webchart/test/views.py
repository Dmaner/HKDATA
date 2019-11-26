from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .resource import Wordresource
from tablib import Dataset
from .models import WORD
import json

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


def columns_view(request):
    dataset = WORD.objects.order_by('-times')

    categories = list()
    appear_times = list()
    for entry in dataset:
        categories.append('%s' % entry.word_text)
        appear_times.append(entry.times)

    test = ['值缺失'] * len(appear_times)

    times_series = {
        'name': "appear times",
        'data': appear_times,
        'color': 'blue',
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': '词对频率图'},
        'xAxis': {'categories': categories},
        'tooltip': {
            'pointFormat': '{series.name}: <br> '
        },
        'series': [times_series]
    }

    dump = json.dumps(chart)

    return render(request, 'words.html', {'chart': dump})


def pieview(request):
    return render(request, 'pieview.html')


def chart_data(request):
    dataset = WORD.objects.order_by('-times')

    series = list()
    total = 0
    for word in dataset[:20]:
        total += word.times
    for word in dataset[:20]:
        series.append({"name": word.word_text, "y": word.times*100/total, "most_common": "值缺失"})

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': '词对图'},
        'tooltip': {
            'pointFormat': '{series.name}: <b>{point.percentage:.1f}% <br> {point.most_common}</br>'
        },
        'plotOptions': {
            'pie': {
                'allowPointSelect': True,
                'cursor': 'pointer',
                'dataLabels': {
                    'enabled': True,
                    'format': '<b>{point.name}</b>: {point.percentage:.1f} % </b>',
                    'color': "(Highcharts.theme & & Highcharts.theme.contrastTextColor) | | 'black'"
                }
            }
        },
        'series': [{
            'name': 'times',
            'data': series,
        }]
    }

    return JsonResponse(chart)


def search():
    return None