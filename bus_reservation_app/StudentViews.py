from django.shortcuts import render, redirect, get_object_or_404
from .models import BusRoute, Schedule, Ticket, Payment, Student, CustomUser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.template.loader import get_template
from datetime import datetime
import json
import requests

def student_home(request):
    return render(request, "student_templates/student_home.html", {})

def make_reservation(request):
    routes = BusRoute.objects.all()
    return render(request, "student_templates/make_reservation.html", {
        "routes": routes,
    })

def bus_schedules(request):
    schedules = Schedule.objects.all()
    return render(request, "student_templates/schedules.html", {
        "schedules": schedules,
    })

@login_required
def search_result(request):
    if request.method == "GET":
        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        date = request.GET.get('date')

        if origin and destination and date:
            # Parse the date string into a datetime object
            try:
                travel_date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return render(request, "student_templates/search_result.html", {
                    "message": "Invalid date format. Please use YYYY-MM-DD."
                })

            # Find routes that match the origin and destination
            routes = BusRoute.objects.filter(Q(origin__iexact=origin) & Q(destination__iexact=destination))

            # Find schedules that match the routes and the given date
            schedules = Schedule.objects.filter(route__in=routes, departure_time__date=travel_date)

            if schedules.exists():
                return render(request, "student_templates/search_result.html", {
                    "schedules": schedules,
                    "date": date,
                })
            else:
                return render(request, "student_templates/search_result.html", {
                    "message": "No Result",
                })
        else:
            return render(request, "student_templates/search_result.html", {
                "message": "Please provide origin, destination, and date."
            })
    else:
        return render(request, "student_templates/search_result.html", {
            "message": "Invalid request method."
        })


def book_seat(request, schedule_id):
    # Retrieve the schedule or return a 404 error if not found
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    # Create a list of available seats based on the capacity of the bus
    seats = [seat for seat in range(1, schedule.bus.capacity + 1)]
    
    return render(request, "student_templates/book_seat.html", {
        "schedule": schedule,
        "seats": seats,
    })
       
@login_required
def get_book_seat(request, schedule_id):
    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        user = request.user.id
        try:
            student = Student.objects.get(admin=user)
        except Student.DoesNotExist:
            # Handle the case where the student doesn't exist
            messages.error(request, "Student not found")
            return redirect("book_seat", schedule_id)

        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            # Handle the case where the schedule doesn't exist
            return HttpResponse("Schedule not found")

        # Check if the seat is already booked
        if Ticket.objects.filter(schedule=schedule, seat_number=seat_number).exists():
            messages.error(request, "Seat already booked")
            return redirect("book_seat", schedule_id)

        # Create a new ticket for the student
        ticket = Ticket.objects.create(student=student, schedule=schedule, seat_number=seat_number, status="pending")
        messages.success(request, "Seat booked successfully")
        return redirect("make_payment", schedule_id)

    else:
        # Handle GET request if needed
        pass


@login_required
def make_payment(request, schedule_id):
    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        amount = request.POST.get('amount')
        user = request.user

        try:
            schedule = Schedule.objects.get(id=schedule_id)
            student = Student.objects.get(admin=user)

            if Ticket.objects.filter(schedule=schedule, seat_number=seat_number).exists():
                messages.error(request, "Seat Already Booked")
                return redirect('book_seat', schedule_id)

            # Generate a unique reference for the payment
            reference = f"{user.id}-{schedule_id}-{seat_number}-{int(datetime.now().timestamp())}"

            # Create a pending ticket
            ticket = Ticket.objects.create(
                student=student,
                schedule=schedule,
                seat_number=seat_number,
                status="pending",
                payment_reference=reference
            )

            # Create a Paystack payment session
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json'
            }
            data = {
                'email': user.email,
                'amount': int(amount) * 100,  # Amount in kobo
                'reference': reference,
                'callback_url': request.build_absolute_uri('/verify_payment/')
            }

            response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=data)
            response_data = response.json()

            if response_data['status']:
                payment_url = response_data['data']['authorization_url']
                return redirect(payment_url)
            else:
                messages.error(request, f"Payment initialization failed: {response_data['message']}")
                return redirect('make_payment', schedule_id)

        except Schedule.DoesNotExist:
            return HttpResponse("Schedule Not Found")
        except Student.DoesNotExist:
            return HttpResponse("Student Not Found")
    else:
        schedule = get_object_or_404(Schedule, id=schedule_id)
        seat_number = request.GET.get('seat_number', 'Unknown')
        amount = 1000  # Placeholder amount; replace with actual amount calculation

        return render(request, "student_templates/payment.html", {
            "schedule": schedule,
            "amount": amount,
            "seat_number": seat_number,
            "paystack_public_key": settings.PAYSTACK_PUBLIC_KEY
        })


@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reference = data.get('reference')
        schedule_id = data.get('schedule_id')
        seat_number = data.get('seat_number')

        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if response_data['status'] and response_data['data']['status'] == 'success':
            # Payment was successful
            amount = response_data['data']['amount'] / 100  # Convert from kobo to naira
            user = request.user
            student = Student.objects.get(admin=user)
            schedule = Schedule.objects.get(id=schedule_id)

            # Create Payment record
            payment = Payment.objects.create(
                student=student,
                schedule=schedule,
                amount=amount,
                payment_status='Paid'
            )

            # Update Ticket record
            ticket = Ticket.objects.get(schedule=schedule, seat_number=seat_number)
            ticket.status = "confirmed",
            ticket.payment = payment
            ticket.payment_reference = reference
            ticket.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'}, status=400)


@login_required
def payment_success(request):
    messages.success(request, "Payment successful! Your seat has been booked.")
    return render(request, "student_templates/payment_success.html")

@login_required
def payment_cancel(request):
    messages.error(request, "Payment was canceled. Please try again.")
    return render(request, "student_templates/payment_cancel.html")

def payment_list(request):
    student = Student.objects.get(admin=request.user)
    payments = Payment.objects.filter(student=student)
    return render(request, "student_templates/payment_list.html", {
        "payments": payments,
    })

def ticket_list(request):
    student = Student.objects.get(admin=request.user)
    tickets = Ticket.objects.filter(student=student)
    return render(request, "student_templates/ticket_list.html", {
        "tickets": tickets,
    })

@login_required
def print_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, student__admin=request.user)
    template = get_template('student_templates/print_ticket.html')
    context = {
        'ticket': ticket,
    }
    html = template.render(context)
    return HttpResponse(html)


def check_email_exists(request):
    pass


    
        

