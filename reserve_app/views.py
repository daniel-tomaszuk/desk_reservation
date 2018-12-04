import redis
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView, View, \
    FormView

from desk_reservation import settings
from reserve_app.forms import DateForm
from reserve_app.models import Reservation, Office, Desk

# create object for connecting wih redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB,
                      decode_responses=True)


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
              str(kwargs.get('name')))
        return HttpResponseRedirect(reverse_lazy('reserve_app:select_date'))


class DateSelect(FormView):
    form_class = DateForm
    template_name = 'reserve_app/date_select.html'
    success_url = reverse_lazy('reserve_app:desk_list')

    def form_valid(self, form):
        if form.is_valid():
            r.set('username_{}:date'.format(self.request.user.username),
                  str(form.cleaned_data.get('date')))
        return super().form_valid(form)


class DeskListView(ListView):
    model = Desk
    template_name = 'reserve_app/desk_list_view.html'

    def get_queryset(self):
        username = self.request.user.username
        selected_city = r.get(f"username_{username}:office")
        selected_date = r.get(f"username_{username}:date")
        query = Desk.objects.filter(office__name=selected_city)\
            .prefetch_related(
            Prefetch('reservations',
                     queryset=Reservation.objects.filter(date=selected_date),
                     to_attr='reservation'))
        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.setdefault('office',
                           r.get(f"username_{self.request.user.username}:office"))
        return context
