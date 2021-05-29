from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    ...

    def save_user(self, request, sociallogin, form=None):
        super(DefaultSocialAccountAdapter, self).save_user(request, sociallogin, form=form)
        # your logic here... and return redirection afterward
        return redirect('accounts/create/profile')
