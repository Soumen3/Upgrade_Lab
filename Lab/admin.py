from django.contrib import admin
from .models import UserDetail
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