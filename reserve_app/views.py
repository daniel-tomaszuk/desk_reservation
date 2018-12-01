from django.views.generic import DetailView

from reserve_app.models import Reservation


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = "reserve_app/reservation_details.html"

    def get_queryset(self):
        user = self.request.user.user
        return Reservation.objects.get(user=user)
