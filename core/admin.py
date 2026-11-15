"""
Django admin configuration for CampusLore.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Category, Question, Answer, Vote,
    Confirmation, Report, Program,
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'college_email', 'branch', 'year', 'account_status',
                    'reputation_score', 'is_profile_complete', 'date_joined')
    list_filter = ('account_status', 'branch', 'year', 'is_profile_complete')
    search_fields = ('username', 'college_email')
    fieldsets = UserAdmin.fieldsets + (
        ('CampusLore Profile', {
            'fields': ('college_email', 'branch', 'year', 'account_status',
                       'reputation_score', 'is_profile_complete'),
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'question_count', 'created_at')
    search_fields = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'anon_display_name', 'status',
                    'answer_count', 'view_count', 'created_date')
    list_filter = ('status', 'category', 'created_date')
    search_fields = ('title', 'description', 'tags')
    readonly_fields = ('anon_display_name', 'view_count')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'anon_display_name', 'helpful_count',
                    'confirmation_count', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('description',)
    readonly_fields = ('anon_display_name', 'helpful_count', 'confirmation_count')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user', 'vote_type', 'created_at')
    list_filter = ('vote_type',)


@admin.register(Confirmation)
class ConfirmationAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user', 'created_at')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_type', 'object_id', 'reporting_user',
                    'reason', 'status', 'created_at')
    list_filter = ('status', 'content_type', 'created_at')
    search_fields = ('reason',)
    actions = ['mark_reviewed', 'mark_resolved', 'mark_dismissed']

    @admin.action(description='Mark selected reports as reviewed')
    def mark_reviewed(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='reviewed', reviewed_at=timezone.now())

    @admin.action(description='Mark selected reports as resolved')
    def mark_resolved(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='resolved', reviewed_at=timezone.now())

    @admin.action(description='Mark selected reports as dismissed')
    def mark_dismissed(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='dismissed', reviewed_at=timezone.now())


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'department', 'batch_size', 'duration_years')
    list_filter = ('department', 'duration_years')
    search_fields = ('name', 'short_name')
