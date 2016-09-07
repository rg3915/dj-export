from django.core.urlresolvers import reverse_lazy as r
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic import UpdateView, DeleteView
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLSX

from djexport.core.admin import PersonResource
from .forms import PersonForm
from .mixins import NameSearchMixin
from .models import Person


def home(request):
    return render(request, 'index.html')


class PersonList(NameSearchMixin, ListView):
    model = Person
    paginate_by = 5


person_detail = DetailView.as_view(model=Person)

person_create = CreateView.as_view(model=Person, form_class=PersonForm)

person_update = UpdateView.as_view(model=Person, form_class=PersonForm)

person_delete = DeleteView.as_view(
    model=Person, success_url=r('core:person_list'))


def export_data_person(request):
    queryset = Person.objects.all()
    return _export_data(queryset, 'person')


def export_data_person_blocked(request):
    queryset = Person.objects.filter(blocked=True)
    return _export_data(queryset, 'person_blocked')


def _export_data(queryset, filename_prefix):
    e = ExportMixin()
    e.resource_class = PersonResource
    e.model = Person
    data = e.get_export_data(XLSX(), queryset)
    response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="{0}.xlsx"'.format(filename_prefix)
    return response
