from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy as r
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic import UpdateView, DeleteView
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLSX
from .mixins import NameSearchMixin
from .models import Person
from .forms import PersonForm
from django.http import HttpResponse


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
    e = ExportMixin()
    e.model = Person
    file_format = XLSX()
    queryset = Person.objects.all()
    data = e.get_export_data(file_format, queryset)
    response = HttpResponse(
        data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="person.xlsx"'
    return response


def export_data_person_blocked(request):
    e = ExportMixin()
    e.model = Person
    file_format = XLSX()
    queryset = Person.objects.all().filter(blocked=True)
    data = e.get_export_data(file_format, queryset)
    response = HttpResponse(
        data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="person_blocked.xlsx"'
    return response
