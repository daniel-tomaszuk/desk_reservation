from django.contrib import admin
from reserve_app.models import Office, Desk, Reservation


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    pass


@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass
