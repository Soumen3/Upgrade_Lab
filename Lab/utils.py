from .models import UserDetail, socialMedia
from django.contrib.auth.models import User

def get_user_all_detail_filled(user):
    context={}
    user_detail = UserDetail.objects.filter(user=user).first()
    if user_detail:
        all_user_details_filled = all([
            user_detail.bio,
            user_detail.location,
            user_detail.birth_date,
            user_detail.profile_pic,
            user_detail.role,
            user_detail.institute
        ])
        context['all_user_details_filled'] = all_user_details_filled
    else:
        context['all_user_details_filled'] = False
    return context

def get_social_media_filled(user):
    context={}
    user_details = UserDetail.objects.filter(user=user).first()
    social_media = socialMedia.objects.filter(user=user_details).first()
    if social_media:
        all_social_media_filled = all([
            social_media.github_username,
            social_media.linkedin_username,
            social_media.twitter_username,
            social_media.facebook_username,
            social_media.instagram_username
        ])
        context['all_social_media_filled'] = all_social_media_filled
    else:
        context['all_social_media_filled'] = False
    return context