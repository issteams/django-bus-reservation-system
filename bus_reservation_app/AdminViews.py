from django.shortcuts import render, redirect
from .models import CustomUser, Student, BusRoute, Bus, Schedule, Payment, Ticket
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def admin_home(request):
    student_count = Student.objects.all().count()
    bus_route_count = BusRoute.objects.all().count()
    bus_count = Bus.objects.all().count()
    schedule_count = Schedule.objects.all().count()
    payment_count = Payment.objects.all().count()
    ticket_count = Ticket.objects.all().count()


    return render(request, "admin_templates/admin_home.html", {
        "student_count": student_count,
        "bus_route_count": bus_route_count,
        "bus_count": bus_count,
        "payment_count": payment_count,
        "schedule_count": schedule_count,
        "ticket_count": ticket_count,
    })


def student(request):
    students = Student.objects.all()
    return render(request, "admin_templates/students.html", {
        "students": students,
    })
    
def add_student(request):
    return render(request, "admin_templates/add_student.html")

    

def add_student_save(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get("password")
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password, user_type=2)
            user.student.phone_number = phone_number
            user.student.address = address
            user.save()
            messages.success(request, "Student Added Successfully!")
            return redirect('add_student')
        except:
            messages.error(request, "Failed to Add Student!")
            return redirect('add_student')
    else:
        return HttpResponse("Method not allowed")

def bus_route(request):
    bus_routes = BusRoute.objects.all()
    return render(request, "admin_templates/bus_route.html", {
        "bus_routes": bus_routes,
    })

def add_bus_route(request):
    return render(request, "admin_templates/add_bus_route.html")

def add_bus_route_save(request):
    if request.method == "POST":
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        distance = request.POST.get('distance')

        try:
            BusRoute.objects.create(origin=origin, destination=destination, distance=distance)
            messages.success(request, "Route Added Successfully!")
            return redirect('add_bus_route')
        except:
            messages.error(request, "Failed to Add Route!")
            return redirect('add_bus_route')
    else:
        return HttpResponse("Method not allowed")
        


def bus(request):
    buses = Bus.objects.all()
    return render(request, "admin_templates/bus.html", {
        "buses": buses,
    })


def add_bus(request):
    bus_routes = BusRoute.objects.all()
    return render(request, "admin_templates/add_bus.html", {
        "bus_routes": bus_routes,
    })

def add_bus_save(request):
    if request.method == "POST":
        bus_number = request.POST.get('bus_number')
        capacity = request.POST.get('capacity')

        try:
            Bus.objects.create(bus_number=bus_number, capacity=capacity)
            messages.success(request, "Bus Added Successfully!")
            return redirect('add_bus')
        except:
            messages.error(request, "Failed to Add Bus!")
            return redirect('add_bus')
    else:
        return HttpResponse("Method not allowed")

def edit_student(request, student_id):
    student = Student.objects.get(admin=student_id)
    return render(request, "admin_templates/edit_student.html", {
        "student": student,
    })

def edit_student_save(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        try:
            #Updating CustomUser Model
            user = CustomUser.objects.get(id=student_id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email 
            user.save()

            # Updating Student Model
            student = Student.objects.get(admin=passenger_id)
            student.address = address
            student.phone_number = phone_number
            student.save()

            messages.success(request, "Student Updated Successfully!")
            return redirect('edit_student', student_id)
        except:
            messages.error(request, "Failed to Update Student!")
            return redirect('edit_student', student_id)
    else:
        return HttpResponse("Method not allowed")
    
def edit_bus_route(request, bus_route_id):
    bus_route = BusRoute.objects.get(id=bus_route_id)
    return render(request, "admin_templates/edit_bus_route.html", {
        "bus_route": bus_route,
    })

def edit_bus_route_save(request):
    if request.method == "POST":
        bus_route_id = request.POST.get('bus_route_id')
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        distance = request.POST.get('distance')

        try:
            bus_route = BusRoute.objects.get(id=bus_route_id)
            bus_route.origin = origin
            bus_route.destination = destination
            bus_route.distance = distance
            bus_route.save()
            messages.success(request, "Route Updated Successfully!")
            return redirect('edit_bus_route', bus_route_id)
        except:
            messages.error(request, "Failed to Update Route!")
            return redirect('edit_bus_route', bus_route_id)
    else:
        return HttpResponse("Method not allowed")
    
    
def edit_bus(request, bus_id):
    bus = Bus.objects.get(id=bus_id)
    return render(request, "admin_templates/edit_bus.html", {
        "bus": bus,
    })

def edit_bus_save(request):
    if request.method == "POST":
        bus_id = request.POST.get('bus_id')
        bus_number = request.POST.get('bus_number')
        capacity = request.POST.get('capacity')

        try:
            bus = Bus.objects.get(id=bus_id)
            bus.bus_number = bus_number
            bus.capacity = capacity
            bus.save()
            messages.success(request, "Bus Updated Successfully!")
            return redirect('edit_bus', bus_id)
        except:
            messages.error(request, "Failed to Update Bus!")
            return redirect('edit_bus', bus_id)
    else:
        return HttpResponse("Method not allowed")


def schedule(request):
    schedules = Schedule.objects.all()
    return render(request, "admin_templates/schedule.html", {
        "schedules": schedules,
    })

def add_schedule(request):
    bus_routes = BusRoute.objects.all()
    buses = Bus.objects.all()
    return render(request, "admin_templates/add_schedule.html", {
        "bus_routes": bus_routes,
        "buses": buses,
    })
    


def add_schedule_save(request):
    if request.method == "POST":
        bus_route_id = request.POST.get('bus_route')
        bus_route = BusRoute.objects.get(id=bus_route_id)
        bus_id = request.POST.get('bus')
        bus = Bus.objects.get(id=bus_id)
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')

        try:
            Schedule.objects.create(route_id=bus_route_id, bus_id=bus_id, departure_time=departure_time, arrival_time=arrival_time)
            messages.success(request, "Schedule Added Successfully!")
            return redirect('add_schedule')
        except:
            messages.error(request, "Failed to Add Schedule!")
            return redirect('add_schedule')
    else:
        return HttpResponse("Method not allowed")

def edit_schedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    bus_routes = BusRoute.objects.all()
    buses = Bus.objects.all()
    return render(request, "admin_templates/edit_schedule.html", {
        "schedule": schedule,
        "bus_routes": bus_routes,
        "buses": buses,
    })
    

def edit_schedule_save(request):
    if request.method == "POST":
        schedule_id = request.POST.get('schedule_id')
        bus_route_id = request.POST.get('bus_route')
        bus_route = BusRoute.objects.get(id=bus_route_id)
        bus_id = request.POST.get('bus')
        bus = Bus.objects.get(id=bus_id)
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')

        try:
            schedule = Schedule.objects.get(id=schedule_id)
            schedule.route = bus_route
            schedule.bus = bus
            schedule.departure_time = departure_time
            schedule.arrival_time = arrival_time
            schedule.save()
            messages.success(request, "Schedule Updated Successfully!")
            return redirect('edit_schedule', schedule_id)
        except:
            messages.error(request, "Failed to Add Schedule!")
            return redirect('edit_schedule', schedule_id)
    else:
        return HttpResponse("Method not allowed")

    

def delete_schedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    schedule.delete()
    messages.error(request, "Schedule Deleted")
    return redirect("schedule")


def delete_student(request, student_id):
    student = CustomUser.objects.get(id=student_id)
    student.delete()
    messages.success(request, "Student Deleted")
    return redirect('students')

def delete_bus_route(request, bus_route_id):
    bus_route = BusRoute.objects.get(id=bus_route_id)
    bus_route.delete()
    messages.success(request, "Route Deleted")
    return redirect("bus_route")

def delete_bus(request, bus_id):
    bus = Bus.objects.get(id=bus_id)
    bus.delete()
    messages.success(request, "Bus Deleted")
    return redirect("bus")

def payment(request):
    payments = Payment.objects.all()
    return render(request, "admin_templates/payment.html", {
        "payments": payments
    })

def add_payment(request):
    students = Student.objects.all()
    schedules = Schedule.objects.all()
    return render(request, "admin_templates/add_payment.html", {
        "students": students,
        "schedules": schedules,
    })
    

def add_payment_save(request):
    if request.method == "POST":
        student_id = request.POST.get('student')
        student = Student.objects.get(admin=student_id)
        schedule_id = request.POST.get('schedule')
        schedule = Schedule.objects.get(id=schedule_id)
        amount = request.POST.get('amount')
        payment_status = request.POST.get('payment_status')

        try:
            Payment.objects.create(student=student, schedule=schedule, amount=amount, payment_status=payment_status)
            messages.success(request, "Payment Added Successfully!")
            return redirect('add_payment')
        except:
            messages.error(request, "Failed to Add Payment!")
            return redirect('add_payment')
    else:
        return HttpResponse("Method not allowed")

def edit_payment(request, payment_id):
    students = Student.objects.all()
    schedules = Schedule.objects.all()
    payment = Payment.objects.get(id=payment_id)
    return render(request, "admin_templates/edit_payment.html", {
        "students": students,
        "schedules": schedules,
        "payment": payment,
    })
    

def edit_payment_save(request):
    if request.method == "POST":
        payment_id = request.POST.get('payment_id')
        student_id = request.POST.get('student')
        student = Student.objects.get(admin=student_id)
        schedule_id = request.POST.get('schedule')
        schedule = Schedule.objects.get(id=schedule_id)
        amount = request.POST.get('amount')
        payment_status = request.POST.get('payment_status')

        try:
            payment = Payment.objects.get(id=payment_id)
            payment.student = student
            payment.schedule_id = schedule
            payment.amount = amount
            payment.payment_status = payment_status
            payment.save()
            messages.success(request, "Payment Updated Successfully!")
            return redirect('edit_payment')
        except:
            messages.error(request, "Failed to Update Payment!")
            return redirect('edit_payment', payment_id)
    else:
        return HttpResponse("Method not allowed")

def delete_payment(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    payment.delete()
    messages.error(request, "Payment Deleted")
    return redirect("payment")


def ticket(request):
    tickets = Ticket.objects.all()
    return render(request, "admin_templates/ticket.html", {
        "tickets": tickets,
    })
    

def add_ticket(request):
    students = Student.objects.all()
    schedules = Schedule.objects.all()
    payments = Payment.objects.all()
    return render(request, "admin_templates/add_ticket.html", {
        "students": students,
        "schedules": schedules,
        "payments": payments,
    })
    
def add_ticket_save(request):
    if request.method == "POST":
        student_id = request.POST.get('student')
        student = Student.objects.get(admin=student_id)
        schedule_id = request.POST.get('schedule')
        schedule = Schedule.objects.get(id=schedule_id)
        payment_id = request.POST.get('payment')
        payment = Payment.objects.get(id=payment_id)
        seat_number = request.POST.get('seat_number')
        status = request.POST.get('status')

        try:
            Ticket.objects.create(student=student, schedule=schedule, payment=payment, status=status, seat_number=seat_number)
            messages.success(request, "Ticket Added Successfully!")
            return redirect('bus_ticketing_app:ticket')
        except:
            messages.error(request, "Failed to Add Ticket!")
            return redirect('bus_ticketing_app:ticket')
    else:
        return HttpResponse("Method not allowed")

def edit_ticket(request, ticket_id):
    students = Student.objects.all()
    schedules = Schedule.objects.all()
    payments = Payment.objects.all()
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, "admin_templates/edit_ticket.html", {
        "students": students,
        "schedules": schedules,
        "payments": payments,
        "ticket": ticket,
    })
    

def edit_ticket_save(request):
    if request.method == "POST":
        ticket_id = request.POST.get('ticket_id')
        student_id = request.POST.get('student')
        student = Student.objects.get(admin=student_id)
        schedule_id = request.POST.get('schedule')
        schedule = Schedule.objects.get(id=schedule_id)
        payment_id = request.POST.get('payment')
        payment = Payment.objects.get(id=payment_id)
        seat_number = request.POST.get('seat_number')
        status = request.POST.get('status')
        ticket_status = Ticket.objects.filter(status=status)

        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.student = student
            ticket.schedule = schedule
            ticket.payment_id = payment
            ticket.seat_number = seat_number
            ticket.status = ticket_status
            ticket.save()
            messages.success(request, "Ticket Updated Successfully!")
            return redirect('edit_ticket')
        except:
            messages.error(request, "Failed to Update Ticket!")
            return redirect('bus_ticketing_app:ticket')
    else:
        return redirect('bus_ticketing_app:ticket')

def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.delete()
    messages.error(request, "Ticket Deleted")
    return redirect("ticket")

def admin_profile(request):
    return render(request, "admin_templates/admin_profile.html", {
    })
    

def admin_profile_save(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = CustomUser.objects.get(id=request.user.id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, "Profile Updated")
        return redirect("admin_profile")
    else:
        return redirect("admin_profile")


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get('email')

    if CustomUser.objects.filter(email=email).exists():
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username = request.POST.get('username')

    if CustomUser.objects.filter(username=username).exists():
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_phone_exist(request):
    phone_number = request.POST.get('phone_number')

    if Student.objects.filter(phone_number=phone_number).exists():
        return HttpResponse(True)
    else:
        return HttpResponse(False)
   