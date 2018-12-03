import redis
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView, View, \
    FormView

from desk_reservation import settings
from reserve_app.forms import DateForm
from reserve_app.models import Reservation, Office

# create object for connecting wih redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


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


class OfficeListView(ListView):
    model = Office
    template_name = 'reserve_app/office_list_view.html'


class OfficeSelect(View):
    def get(self, request, *args, **kwargs):
        r.set('username_{}:office'.format(request.user.username),
              str(kwargs.get('pk')))
        return HttpResponseRedirect(reverse_lazy('reserve_app:select_date'))


class DateSelect(FormView):
    form_class = DateForm
    template_name = 'reserve_app/date_select.html'
    success_url = reverse_lazy('reserve_app:reservation_details')

    def form_valid(self, form):
        if form.is_valid():
            r.set('username_{}:date'.format(self.request.user.username),
                  str(form.cleaned_data.get('date')))
        return super().form_valid(form)


