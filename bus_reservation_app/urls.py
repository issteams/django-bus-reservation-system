from django.urls import path, include
from . import views, AdminViews, StudentViews


urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('auth-signin/', views.auth_signin, name='auth-signin'),
    path('auth/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('auth-signup/', views.auth_signup, name='auth-signup'),

    # Admin Paths
    path('admin_home/', AdminViews.admin_home, name='admin_home'),
    path('students/', AdminViews.student, name='students'),
    path('students/add_student/', AdminViews.add_student, name='add_student'),
    path('students/add_student_save/', AdminViews.add_student_save, name='add_student_save'),
    path('students/edit_student/<str:student_id>/', AdminViews.edit_student, name='edit_student'),
    path('students/edit_student_save/', AdminViews.edit_student_save, name='edit_student_save'),
    path('students/delete_student/<str:student_id>/', AdminViews.delete_student, name='delete_student'),
    path('bus_route/', AdminViews.bus_route, name='bus_route'),
    path('bus_route/add_bus_route/', AdminViews.add_bus_route, name='add_bus_route'),
    path('bus_route/add_bus_route_save/', AdminViews.add_bus_route_save, name='add_bus_route_save'),
    path('bus_route/edit_bus_route/<str:bus_route_id>/', AdminViews.edit_bus_route, name='edit_bus_route'),
    path('bus_route/edit_bus_route_save/', AdminViews.edit_bus_route_save, name='edit_bus_route_save'),
    path('bus_route/delete_bus_route/<str:bus_route_id>/', AdminViews.delete_bus_route, name='delete_bus_route'),
    path('bus/', AdminViews.bus, name='bus'),
    path('bus/add_bus/', AdminViews.add_bus, name='add_bus'),
    path('bus/add_bus_save/', AdminViews.add_bus_save, name='add_bus_save'),
    path('bus/edit_bus/<str:bus_id>/', AdminViews.edit_bus, name='edit_bus'),
    path('bus/edit_bus_save/', AdminViews.edit_bus_save, name='edit_bus_save'),
    path('bus/delete_bus/<str:bus_id>', AdminViews.delete_bus, name='delete_bus'),
    path('schedule/', AdminViews.schedule, name='schedule'),
    path('schedule/add_schedule/', AdminViews.add_schedule, name='add_schedule'),
    path('schedule/add_schedule_save/', AdminViews.add_schedule_save, name='add_schedule_save'),
    path('schedule/edit_schedule/<str:schedule_id>/', AdminViews.edit_schedule, name='edit_schedule'),
    path('schedule/edit_schedule_save/', AdminViews.edit_schedule_save, name='edit_schedule_save'),
    path('schedule/delete_schedule/<str:schedule_id>', AdminViews.delete_schedule, name='delete_schedule'),
    path('payment/', AdminViews.payment, name='payment'),
    path('payment/add_payment/', AdminViews.add_payment, name='add_payment'),
    path('payment/add_payment_save/', AdminViews.add_payment_save, name='add_payment_save'),
    path('payment/edit_payment/<str:payment_id>/', AdminViews.edit_payment, name='edit_payment'),
    path('payment/edit_payment_save/', AdminViews.edit_payment_save, name='edit_payment_save'),
    path('payment/payment/delete_payment/<str:payment_id>/', AdminViews.delete_payment, name='delete_payment'),
    path('ticket/', AdminViews.ticket, name='ticket'),
    path('ticket/add_ticket/', AdminViews.add_ticket, name='add_ticket'),
    path('ticket/add_ticket_save/', AdminViews.add_ticket_save, name='add_ticket_save'),
    path('ticket/edit_ticket/<str:ticket_id>/', AdminViews.edit_ticket, name='edit_ticket'),
    path('ticket/edit_ticket_save/', AdminViews.edit_ticket_save, name='edit_ticket_save'),
    path('ticket/delete_ticket/<str:ticket_id>/', AdminViews.delete_ticket, name='delete_ticket'),
    path('admin_profile/', AdminViews.admin_profile, name='admin_profile'),
    path('admin_profile_save/', AdminViews.admin_profile_save, name='admin_profile_save'),

    # Student Paths
   path('student_home/', StudentViews.student_home, name='student_home'),
   path('bus_schedules/', StudentViews.bus_schedules, name='schedules'),
   path('make_reservation/', StudentViews.make_reservation, name='make_reservation'),
   path("search_result/", StudentViews.search_result, name='search_result'),
   path("book_seat/<str:schedule_id>/", StudentViews.book_seat, name='book_seat'),
   path("get_book_seat/<str:schedule_id>/", StudentViews.get_book_seat, name='get_book_seat'),
   path("make_payment/schedule_id=<str:schedule_id>/", StudentViews.make_payment, name='make_payment'),
   path("comfirm_payment/<str:payment_id>/", StudentViews.comfirm_payment, name='comfirm_pament'),



    path('logout/', views.user_logout, name='logout'),
]
