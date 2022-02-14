from django.urls import path
from timekeeping.views import TimeTableView, TimeInputPartialView

app_name = 'timekeeping'

urlpatterns = [
    path('', TimeTableView.as_view(), name='time-table'),
    path('create/', TimeInputPartialView.as_view(), name='time-input'),
]