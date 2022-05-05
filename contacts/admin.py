from django.contrib import admin
from .models import Person, DeletedContacts

class PersonAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'email', 'phone', 'is_archived', 'slug', 'qr_code']
    list_display = ['name', 'email', 'phone', 'slug', 'is_archived', 'qr_code']
    readonly_fields = ['slug', 'qr_code']


class DeletedContactsAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'email', 'phone', 'is_archived', 'slug']
    list_display = ['name', 'email', 'phone', 'slug', 'is_archived']
    readonly_fields = ['slug']


admin.site.register(Person, PersonAdmin)
admin.site.register(DeletedContacts, DeletedContactsAdmin)

# Register your models here.
