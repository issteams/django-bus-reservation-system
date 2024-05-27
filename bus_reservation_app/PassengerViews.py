from django.shortcuts import render, redirect
from .models import BusRoute, Schedule, Ticket, Payment, Passenger
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime


def passenger_home(request):
    return render(request, "passenger_templates/passenger_home.html", {})

@login_required
def search_result(request):
    if request.method == "GET":
        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        date = request.GET.get('date')

        routes = BusRoute.objects.filter(origin=origin, destination=destination)

        if routes != None:
            return render(request, "bus_ticketing_app/users/search_result.html", {
                "routes": routes,
                "date": date,
            })
        else:
            return render(request, "bus_ticketing_app/users/search_result.html", {
                    "message": "No Result",
                })
    else:
        pass



@login_required
def select_schedule(request, route_id, date):
    schedules = Schedule.objects.filter(route_id=route_id, departure_time__date=date)
    schedule_id = None
    departure_time = None
    arrival_time = None
    # available_seats = 0
    capacity = 0
    seats = []

    for schedule in schedules:
        schedule_id = schedule.id
        departure_time = schedule.departure_time
        arrival_time = schedule.arrival_time
        capacity = schedule.bus_id.capacity
        # booked_seats = schedule.ticket_set.values_list('seat_number', flat=True)
        # available_seats = capacity - len(booked_seats)
        for seat in range(1, capacity + 1):
            seats.append(seat)

    # if selected_seat:
    #     if selected_seat in seats:
    #         seats.remove(selected_seat)
    #         available_seats -= 1
    #         # Update bus capacity in the database
    #         schedule.bus_id.capacity -= 1
    #         schedule.bus_id.save()
    #         print("Seat booked successfully")
    #         # Add your booking logic here
    #     else:
    #         print("Selected seat is not available")

    return render(request, "bus_ticketing_app/users/schedule.html", {
        "schedule_id": schedule_id,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "capacity": capacity,
        "seats": seats,
    })


def book_seat(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    seats = []
    schedule_id = schedule.id
    capacity = schedule.bus_id.capacity
    for seat in range(1, capacity + 1):
        seats.append(seat)
    return render(request, "bus_ticketing_app/users/book_seat.html", {
        "schedule_id": schedule_id,
        "seats": seats,
    })
       
@login_required
def get_book_seat(request, schedule_id):
    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        user = request.user.id
        passenger = Passenger.objects.get(admin=user)
        try:
            schedule = Schedule.objects.get(id=schedule_id)
            if Ticket.objects.filter(schedule=schedule, seat_number=seat_number).exists():
                messages.error(request, "Seat Already Booked")
                return redirect("bus_ticketing_app:book_seat", schedule_id)
            else:
                Ticket.objects.create(passenger_id=passenger, schedule=schedule, seat_number=seat_number, status="pending")
                messages.success(request, "Seat Booked Sucessfuly")
                return redirect("bus_ticketing_app:make_payment", schedule_id)
        except Schedule.DoesNotExist:
            return HttpResponse("Not Found")
    else:
        pass


@login_required
def make_payment(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    return render(request, "bus_ticketing_app/users/payment.html", {})
    
    # if request.method == 'POST':
    #     user = request.user.id
    #     try:
    #         schedule = Schedule.objects.get(pk=schedule_id)
    #         payment = Payment.objects.create(passenger_id=user, schedule_id=schedule, amount=amount, payment_status="Pending")
    #         return HttpResponse("Payment Created Successfully")
    #     except Schedule.DoesNotExist:
    #         return HttpResponse("Not Found")

@login_required
def comfirm_payment(request, payment_id):
    if request.method == 'POST':
        try:
            payment = Payment.objects.get(pk=payment_id)
            payment.payment_status = 'Paid'
            payment.save()

            Ticket.objects.filter(payment=payment).update(status="comfirmed")
            return HttpResponse("Payment Comfirmed")
        except Payment.DoesNotExist:
            return HttpResponse("Not Found")




    
        

