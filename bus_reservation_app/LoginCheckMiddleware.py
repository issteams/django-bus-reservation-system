from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class LoginCheckMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        logger.info(f"Module name: {modulename}")
        user = request.user

        # Paths that do not require redirection for unauthenticated users
        allowed_paths = [
            reverse("index"),
            reverse("signin"),
            reverse("auth-signin"),
            reverse("signup"),
            reverse("auth-signup"),
            reverse("password_reset"),
            reverse("password_reset_done"),
            reverse("password_reset_confirm", kwargs={'uidb64': 'uid', 'token': 'token'}),
            reverse("password_reset_complete"),
        ]

        # Logic for authenticated users
        if user.is_authenticated:
            if user.user_type == 1:  # Admin user
                if request.path == reverse("admin_home") or modulename in [
                    "bus_reservation_app.AdminViews",
                    "bus_reservation_app.views",
                    "django.views.static",
                    "django.contrib.auth.views",
                    "django.contrib.admin.sites",
                    "django.contrib.admin.options"
                ]:
                    return None
                else:
                    logger.info("Redirecting authenticated admin user to admin_home")
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == 2:  # Student user
                if request.path == reverse("student_home") or modulename in [
                    "bus_reservation_app.UserViews",
                    "bus_reservation_app.views",
                    "django.views.static"
                ]:
                    return None
                else:
                    logger.info("Redirecting authenticated student user to passenger_home")
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                logger.info("Redirecting authenticated user with unknown type to signin")
                return HttpResponseRedirect(reverse('signin'))

        # Logic for unauthenticated users
        else:
            if request.path in allowed_paths or modulename in [
                "django.contrib.auth.views",
                "django.contrib.admin.sites",
                "bus_reservation_app.views"
            ]:
                return None
            else:
                logger.info("Redirecting unauthenticated user to auth-signin")
                return HttpResponseRedirect(reverse("signin"))

        return None  # Continue processing the request if no redirection is required
