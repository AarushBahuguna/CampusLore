"""
Middleware for CampusLore.
"""

from django.shortcuts import redirect
from django.urls import reverse


class ProfileCompleteMiddleware:
    """
    Redirect authenticated users with incomplete profiles to the profile
    completion page. Allows access to logout, admin, static, and the
    profile-complete page itself.
    """

    EXEMPT_URLS = [
        '/accounts/',
        '/admin/',
        '/static/',
        '/profile/complete/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            if not request.user.is_profile_complete:
                # Allow certain URLs without redirect
                path = request.path
                if not any(path.startswith(url) for url in self.EXEMPT_URLS):
                    return redirect(reverse('profile_complete'))
        return self.get_response(request)
