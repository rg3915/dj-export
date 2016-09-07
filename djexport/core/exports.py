from datetime import datetime
from django.http import HttpResponse
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLSX

from djexport.core.admin import PersonResource
from .models import Person


def export_data_person(request):
    queryset = Person.objects.all()
    return _export_data(queryset, 'person')


def export_data_person_blocked(request):
    queryset = Person.objects.filter(blocked=True)
    return _export_data(queryset, 'person-blocked')


def _export_data(queryset, filename_prefix):
    e = ExportMixin()
    e.resource_class = PersonResource
    e.model = Person
    data = e.get_export_data(XLSX(), queryset)
    mdata = datetime.now().strftime('%Y-%m-%d')
    response = HttpResponse(
        data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response[
        'Content-Disposition'] = 'attachment; filename="{0}-{1}.xlsx"'.format(filename_prefix, mdata)
    return response
