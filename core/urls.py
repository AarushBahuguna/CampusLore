"""
URL patterns for the core app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('questions/', views.question_list, name='question_list'),
    path('questions/<int:pk>/', views.question_detail, name='question_detail'),
    path('college/', views.college_info, name='college_info'),
    path('programs/', views.programs, name='programs'),
    path('search/', views.search, name='search'),

    # AJAX endpoints
    path('api/search/', views.ajax_search, name='ajax_search'),
    path('api/similar-questions/', views.ajax_similar_questions, name='ajax_similar_questions'),

    # Authenticated - Profile
    path('profile/', views.profile, name='profile'),
    path('profile/complete/', views.profile_complete, name='profile_complete'),

    # Authenticated - Questions
    path('questions/new/', views.question_create, name='question_create'),
    path('questions/<int:pk>/edit/', views.question_edit, name='question_edit'),
    path('questions/<int:pk>/delete/', views.question_delete, name='question_delete'),
    path('questions/<int:pk>/resolve/', views.question_resolve, name='question_resolve'),

    # Authenticated - Answers
    path('questions/<int:question_pk>/answer/', views.answer_create, name='answer_create'),
    path('answers/<int:pk>/edit/', views.answer_edit, name='answer_edit'),
    path('answers/<int:pk>/delete/', views.answer_delete, name='answer_delete'),

    # Authenticated - Voting & Confirmation (AJAX)
    path('answers/<int:pk>/vote/', views.vote_answer, name='vote_answer'),
    path('answers/<int:pk>/confirm/', views.confirm_answer, name='confirm_answer'),

    # Authenticated - Reporting
    path('report/<str:content_type>/<int:object_id>/', views.report_content, name='report_content'),

    # Superuser - Reports
    path('admin-reports/', views.admin_reports, name='admin_reports'),
    path('admin-reports/csv/', views.export_csv, name='export_csv'),
    path('admin-reports/pdf/', views.export_pdf, name='export_pdf'),
]
