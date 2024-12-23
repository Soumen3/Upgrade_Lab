from django.contrib import admin
from .models import UserDetail, socialMedia
# Register your models here.


# @admin.register(institue)
# class institueAdmin(admin.ModelAdmin):
#     list_display = ['name', 'location', 'phone']
#     search_fields = ['name', 'location']

@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'institute', 'created_at']
    search_fields = ['user__username', 'role', 'institute']
    list_filter = ['role', 'institute']
    list_editable = ['role', 'institute']
    list_per_page = 10
    list_display_links = ['user']
    list_select_related = ['user']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'bio', 'profile_pic')
        }),
        ('Additional Info', {
            'fields': ('location', 'birth_date', 'role', 'institute')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )
    add_fieldsets = (
        ('User Info', {
            'fields': ('user', 'bio', 'profile_pic')
        }),
        ('Additional Info', {
            'fields': ('location', 'birth_date', 'role', 'institute')
        }),
    )
    actions = ['make_teacher', 'make_student']

    def make_teacher(self, request, queryset):
        queryset.update(role='teacher')

    make_teacher.short_description = "Mark selected users as teacher"

    def make_student(self, request, queryset):
        queryset.update(role='student')

    make_student.short_description = "Mark selected users as student"


@admin.register(socialMedia)
class socialMediaAdmin(admin.ModelAdmin):
    list_display = ['user', 'github_username', 'linkedin_username', 'twitter_username', 'facebook_username', 'instagram_username']
    search_fields = ['user__user__username', 'github_username', 'linkedin_username', 'twitter_username', 'facebook_username', 'instagram_username']
    list_filter = ['github_username', 'linkedin_username', 'twitter_username', 'facebook_username', 'instagram_username']
    list_editable = ['github_username', 'linkedin_username', 'twitter_username', 'facebook_username', 'instagram_username']
    list_per_page = 10
    list_display_links = ['user']
    list_select_related = ['user']
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Social Media', {
            'fields': ('github_username', 'linkedin_username', 'twitter_username', 'facebook_username', 'instagram_username')
        })
    )
    add_fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Social Media', {
            'fields': ('github_username', 'linkedin_username', 'twitter_username', 'facebook_username', 'instagram_username')
        })
    )
    actions = ['clear_github', 'clear_linkedin', 'clear_twitter', 'clear_facebook', 'clear_instagram']

    def clear_github(self, request, queryset):
        queryset.update(github_username='')

    clear_github.short_description = "Clear github username"

    def clear_linkedin(self, request, queryset):
        queryset.update(linkedin_username='')

    clear_linkedin.short_description = "Clear linkedin username"

    def clear_twitter(self, request, queryset):
        queryset.update(twitter_username='')

    clear_twitter.short_description = "Clear twitter username"

    def clear_facebook(self, request, queryset):
        queryset.update(facebook_username='')

    clear_facebook.short_description = "Clear facebook username"

    def clear_instagram(self, request, queryset):
        queryset.update(instagram_username='')

    clear_instagram.short_description = "Clear instagram username"