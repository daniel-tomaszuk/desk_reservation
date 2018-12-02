from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView
from django.views.generic.base import View

from reserve_app.models import Reservation


class ReservationDetailView(ListView):
    model = Reservation
    template_name = "reserve_app/reservation_details.html"

    def get_queryset(self):
        username = self.request.user.username
        try:
            qs = Reservation.objects.get(user__username=username)
        except Reservation.DoesNotExist:
            qs = []
        return qs

    def post(self, request):
        reservation = get_object_or_404(Reservation, id=request.kwargs.get('pk'))
        reservation.confirm = True
        reservation.save()
        return reverse_lazy('reserve_app:reservation_details')


class DeleteReservation(DeleteView):
    model = Reservation
    success_url = reverse_lazy('reserve_app:reservation_details')


class ConfirmReservation(UpdateView):
    model = Reservation
    fields = ['confirmed']
    success_url = reverse_lazy('reserve_app:reservation_details')

    # def post(self, request, *args, **kwargs):
    #     reservation = get_object_or_404(Reservation, id=kwargs.get('pk'))
    #     reservation.confirmed = True
    #     reservation.save()
    #     return super().post(request, *args, **kwargs)
