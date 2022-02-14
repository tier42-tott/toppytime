import datetime
import logging

from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .models import TimeEntry
from .forms import TimeEntryForm


class TimeTableView(TemplateView):
    template_name = 'timekeeping/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # https://stackoverflow.com/questions/18200530/get-the-last-sunday-and-saturdays-date-in-python
        today = datetime.date.today()
        idx = (today.weekday() + 1) % 7
        sun = today - datetime.timedelta(7 + idx)
        # https://stackoverflow.com/questions/4668619/how-do-i-filter-query-objects-by-date-range-in-django
        context['time_entries'] = TimeEntry.objects.filter(end_time__gte=sun)
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
            time_entry = form.save()
            context = {
                'time_entry': time_entry
            }
            return render(request, 'timekeeping/partials/time_entry_row.html', context)
        # if form had errors, resend the form partial to have the user fix them
        context = {
            'form': form
        }
        print("Invalid Form")
        print(form.errors)
        return render(request, 'timekeeping/partials/create_time_entry.html', context)
