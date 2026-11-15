"""
Custom allauth adapters to restrict authentication to @mail.jiit.ac.in emails.
"""

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect


ALLOWED_EMAIL_DOMAIN = 'mail.jiit.ac.in'


class JIITAccountAdapter(DefaultAccountAdapter):
    """Restrict regular account signup to JIIT emails only."""

    def is_open_for_signup(self, request):
        return True

    def clean_email(self, email):
        email = super().clean_email(email)
        if not email.endswith(f'@{ALLOWED_EMAIL_DOMAIN}'):
            from django.core.exceptions import ValidationError
            raise ValidationError(
                f'Only @{ALLOWED_EMAIL_DOMAIN} email addresses are allowed.'
            )
        return email


class JIITSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Restrict Google OAuth to JIIT emails only."""

    def is_open_for_signup(self, request, sociallogin):
        return True

    def pre_social_login(self, request, sociallogin):
        """Check email domain before allowing social login."""
        email = sociallogin.account.extra_data.get('email', '')
        if not email.endswith(f'@{ALLOWED_EMAIL_DOMAIN}'):
            from django.contrib import messages
            messages.error(
                request,
                f'Only @{ALLOWED_EMAIL_DOMAIN} email addresses are allowed. '
                f'Please use your JIIT college email to sign in.'
            )
            raise Exception(f'Email domain not allowed: {email}')

    def populate_user(self, request, sociallogin, data):
        """Populate user fields from Google account data."""
        user = super().populate_user(request, sociallogin, data)
        email = data.get('email', '')
        user.college_email = email
        return user
