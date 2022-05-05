from django.urls import path
from . import views

urlpatterns = [
    path('', views.contactList),
    path('details/<slug:slug>/', views.details),
    path('addcontact/',views.addcontact),
    path('my_account/',views.my_account),
    path('shear/<slug:slug>/', views.qr_code),
    path('trashcontact/',views.trashcontact),

    # api
    path('contact_list_api/', views.contact_list_api.as_view()),
    path('details_api/<slug:slug>/', views.DetailsApi.as_view()),
    path('contact_edit_api/<slug:slug>/', views.contact_edit_api.as_view()),
    path('addcontact_api/',views.Add_contact_api.as_view()),

    path('my_account_api/',views.My_account_api.as_view()),
    path('edit_my_account_api/',views.My_account_edit_api.as_view()),

    path('trash_list_api/',views.Trash_contact_list_api.as_view()),
    path('trash_contact_api/<slug:slug>/',views.Trash_contact_api.as_view()),
    path('trash_restore_api/<slug:slug>/',views.Trash_restore.as_view()),

    path('deletecontact_api/<slug:slug>/',views.Delete_contact_api.as_view()),
    path('search_contacts_api/',views.Search_contact_api.as_view()),
]

