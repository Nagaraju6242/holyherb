from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Override the DefaultSocialAccountAdapter from allauth in order to associate
    the social account with a matching User automatically, skipping the email
    confirm form and existing email error
    """
    def pre_social_login(self, request, sociallogin):
        print(sociallogin)
        print(sociallogin.user)
        print(sociallogin.user.email)
        user = User.objects.filter(email=sociallogin.user.email).first()
        if user and not sociallogin.is_existing:
            print(sociallogin)
            sociallogin.connect(request, user)


