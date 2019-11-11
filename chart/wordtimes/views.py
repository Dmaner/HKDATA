from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from .resource import Wordresource
from tablib import Dataset
from .models import WORD
import json

# Create your views here.
global search_name

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
    global search_name
    search_name = 'aaronMCN'
    return render(request, 'home.html')


def pieview(request):
    return render(request, 'pieview.html')


def chart_data(request):
    # name = 'aaronMCN'
    name = search_name
    dataset = WORD.objects.filter(belong=name).order_by('-times')

    series = list()
    fans = 0
    total = 0
    for word in dataset:
        if fans == 0:
            fans = word.fans
        total += word.times
    for word in dataset:
        series.append({"name": word.word_text, "y": word.times*100/total,
                       "relate_1": word.relate_1, "relate_2":word.relate_2,
                       "relate_3": word.relate_3, "relate_4": word.relate_4,
                       "relate_5": word.relate_5,
                       })

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': '{}(粉丝数 {})词对图'.format(name, fans)},
        'tooltip': {
            'pointFormat': '<b>{series.name}</b>: {point.percentage:.1f}% '
                           '<br>关联词</br><br> {point.relate_1}</br>'
                           '<br> {point.relate_2}</br><br>{point.relate_3}</br>'
                           '<br> {point.relate_4}</br><br> {point.relate_5}</br>'
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

def search_form(request):
    return render_to_response('search.html')


def search(request):
    if 'q' in request.GET:
        global search_name
        search_name = request.GET['q']
        return pieview(request)
    else:
        message = 'You submitted an empty form.'
        return HttpResponse(message)