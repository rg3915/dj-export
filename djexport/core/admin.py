from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .forms import PersonForm
from .models import Person, Phone

PERSONFIELDS = ('first_name', 'last_name', 'email', 'blocked', 'created')


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 1


class PersonResource(resources.ModelResource):

    class Meta:
        model = Person
        fields = PERSONFIELDS
        export_order = PERSONFIELDS
        widgets = {
            'created': {'format': '%d/%m/%Y %H:%M'},
        }


@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    inlines = [PhoneInline]
    resource_class = PersonResource
    list_display = ('__str__', 'email', 'phone', 'uf', 'created', 'blocked')
    date_hierarchy = 'created'
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = (
        # 'uf',
        ('created', DateRangeFilter),
    )
    form = PersonForm

    def phone(self, obj):
        return obj.phone_set.first()

    phone.short_description = 'telefone'
