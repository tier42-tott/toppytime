import datetime

from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .models import TimeEntry
from .forms import TimeEntryForm


def get_sunday(date):
    # https://stackoverflow.com/questions/18200530/get-the-last-sunday-and-saturdays-date-in-python
    idx = (date.weekday() + 1) % 7
    sun = date - datetime.timedelta(idx)
    return sun


class TimeTableView(TemplateView):
    template_name = 'timekeeping/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # https://stackoverflow.com/questions/4668619/how-do-i-filter-query-objects-by-date-range-in-django
        context['time_entries'] = TimeEntry.objects.filter(end_time__gte=get_sunday(datetime.date.today()))
        context['total_hours'] = sum(t.hours() for t in context['time_entries'])
        form = TimeEntryForm()
        context['form'] = form
        return context


class TimeInputPartialView(View):
    def get_model(self):
        model = None
        if self.request.GET:
            product_id = self.request.GET.get('id', None)
            if product_id:
                model = TimeEntry.objects.get(pk=product_id)
        return model

    def get_form(self):
        if self.request.POST:
            form = TimeEntryForm(self.request.POST)
        else:
            initial_model = self.get_model()
            form = TimeEntryForm(instance=initial_model)
        return form

    def get(self, request):
        context = {
            'form': self.get_form()
        }
        return render(request, 'timekeeping/partials/', context)

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            print('Form is valid!')
            form.save()
            form = TimeEntryForm()
        today = datetime.date.today()
        idx = (today.weekday() + 1) % 7
        sun = today - datetime.timedelta(idx)
        context = {
            'time_entries': TimeEntry.objects.filter(end_time__gte=get_sunday(datetime.date.today())),
            'form': form
        }
        context['total_hours'] = sum(t.hours() for t in context['time_entries'])
        return render(request, 'timekeeping/partials/time_entry_form_post.html', context)
