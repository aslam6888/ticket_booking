from django.urls import path
from . import views


urlpatterns=[
    path('',views.home),
    path('admin-page',views.admin_view),
    path('agent/delete/<int:id>',views.delete_agent),
    path('booking',views.booking_view),
    path('seat-available/<str:train>/<str:date>',views.seat_bookings),
    path('add/newtrain',views.add_train),
    path('add/chart',views.chart_list),
    path('agent/bookings',views.agent_booking_view),
    path('agent/seatings/<int:id>',views.agent_seating_view),
    path('login',views.login_view),
    path('logout',views.logout_view),
]