"""desk_reservation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from reserve_app.views import ReservationDetailView, DeleteReservation, \
    ConfirmReservation, OfficeListView, OfficeSelect, DateSelect, DeskListView

app_name = "reserve_app"
urlpatterns = [
    path('', ReservationDetailView.as_view(), name='reservation_details'),
    path('cancel_reservation/<int:pk>/', DeleteReservation.as_view(), name='reservation_delete'),
    path('confirm_reservation/<int:pk>/', ConfirmReservation.as_view(), name='reservation_confirm'),
    path('offices_list/', OfficeListView.as_view(), name='office_list'),
    path('select_office/<str:name>/', OfficeSelect.as_view(), name='select_office'),
    path('select_date/', DateSelect.as_view(), name='select_date'),
    path('desk_list/', DeskListView.as_view(), name='desk_list'),

]
