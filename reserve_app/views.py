from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from reserve_app.models import Reservation


class ReservationDetailView(ListView):
    model = Reservation
    template_name = "reserve_app/reservation_details.html"

    def get_queryset(self):
        username = self.request.user.username
        qs = get_object_or_404(Reservation, user__username=username)
        return qs
