from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy as r
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic import UpdateView, DeleteView
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLSX
from .mixins import NameSearchMixin
from .models import Person
from .forms import PersonForm


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
    return e.get_export_data(file_format, queryset)
