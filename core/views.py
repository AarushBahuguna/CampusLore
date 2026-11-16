"""
Views for CampusLore.
"""

import csv
import io
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.db.models import Q, Count
from django.utils import timezone
from django.core.paginator import Paginator

from django.db import models as db_models

from .models import (
    CustomUser, Category, Question, Answer, Vote,
    Confirmation, Report, Program,
)
from .forms import QuestionForm, AnswerForm, ReportForm, ProfileCompleteForm
from .college_data import COLLEGE_INFO


# ---------------------------------------------------------------------------
# Public Views
# ---------------------------------------------------------------------------

def home(request):
    """Dashboard / Home page - public."""
    recent_questions = Question.objects.select_related('category', 'author')[:10]
    popular_questions = Question.objects.annotate(
        num_answers=Count('answers')
    ).order_by('-view_count', '-num_answers')[:10]
    unanswered_questions = Question.objects.annotate(
        num_answers=Count('answers')
    ).filter(num_answers=0)[:10]
    categories = Category.objects.annotate(
        num_questions=Count('questions')
    ).order_by('-num_questions')[:10]

    context = {
        'recent_questions': recent_questions,
        'popular_questions': popular_questions,
        'unanswered_questions': unanswered_questions,
        'categories': categories,
        'total_questions': Question.objects.count(),
        'total_answers': Answer.objects.count(),
        'total_users': CustomUser.objects.filter(is_profile_complete=True).count(),
    }
    return render(request, 'core/home.html', context)


def question_list(request):
    """List all questions with filtering and sorting - public."""
    questions = Question.objects.select_related('category', 'author').annotate(
        num_answers=Count('answers')
    )

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        questions = questions.filter(category_id=category_id)

    # Filter by status
    status = request.GET.get('status')
    if status in ('open', 'resolved', 'closed'):
        questions = questions.filter(status=status)

    # Filter by tag
    tag = request.GET.get('tag')
    if tag:
        questions = questions.filter(tags__icontains=tag)

    # Sort
    sort = request.GET.get('sort', 'newest')
    if sort == 'oldest':
        questions = questions.order_by('created_date')
    elif sort == 'popular':
        questions = questions.order_by('-view_count', '-num_answers')
    elif sort == 'most_answers':
        questions = questions.order_by('-num_answers')
    elif sort == 'unanswered':
        questions = questions.filter(num_answers=0).order_by('-created_date')
    else:  # newest
        questions = questions.order_by('-created_date')

    paginator = Paginator(questions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_id,
        'current_sort': sort,
        'current_status': status,
        'current_tag': tag,
    }
    return render(request, 'core/question_list.html', context)


def question_detail(request, pk):
    """View a single question and its answers - public."""
    question = get_object_or_404(
        Question.objects.select_related('category', 'author'), pk=pk
    )
    # Increment view count
    Question.objects.filter(pk=pk).update(view_count=db_models.F('view_count') + 1)
    question.refresh_from_db()

    answers = question.answers.select_related('contributor').prefetch_related(
        'votes', 'confirmations'
    )
    answer_form = AnswerForm()

    context = {
        'question': question,
        'answers': answers,
        'answer_form': answer_form,
    }
    return render(request, 'core/question_detail.html', context)


def college_info(request):
    """Display hardcoded JIIT college information - public."""
    return render(request, 'core/college_info.html', {'college': COLLEGE_INFO})


def programs(request):
    """Display programs offered at JIIT - public."""
    programs_list = Program.objects.all()
    return render(request, 'core/programs.html', {'programs': programs_list})


def search(request):
    """Search questions - public."""
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category')
    status = request.GET.get('status')

    results = Question.objects.select_related('category').annotate(
        num_answers=Count('answers')
    )

    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )

    if category_id:
        results = results.filter(category_id=category_id)

    if status:
        results = results.filter(status=status)

    paginator = Paginator(results, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'current_category': category_id,
        'current_status': status,
    }
    return render(request, 'core/search_results.html', context)


# ---------------------------------------------------------------------------
# AJAX Views (public - return JSON)
# ---------------------------------------------------------------------------

def ajax_search(request):
    """AJAX live search endpoint - returns JSON."""
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': []})

    questions = Question.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(tags__icontains=query)
    ).values('id', 'title', 'category__name', 'status')[:8]

    results = [
        {
            'id': q['id'],
            'title': q['title'],
            'category': q['category__name'],
            'status': q['status'],
        }
        for q in questions
    ]
    return JsonResponse({'results': results})


def ajax_similar_questions(request):
    """AJAX similar question suggestions (while creating a new question)."""
    title = request.GET.get('title', '').strip()
    if len(title) < 5:
        return JsonResponse({'suggestions': []})

    # Simple keyword matching - split title into words and search
    words = [w for w in title.split() if len(w) > 2]
    q_filter = Q()
    for word in words[:5]:  # Limit to first 5 significant words
        q_filter |= Q(title__icontains=word)

    if not q_filter:
        return JsonResponse({'suggestions': []})

    questions = Question.objects.filter(q_filter).values(
        'id', 'title', 'status'
    ).distinct()[:5]

    suggestions = [
        {
            'id': q['id'],
            'title': q['title'],
            'status': q['status'],
        }
        for q in questions
    ]
    return JsonResponse({'suggestions': suggestions})


# ---------------------------------------------------------------------------
# Authenticated Views (login required)
# ---------------------------------------------------------------------------

@login_required
def profile(request):
    """User profile page."""
    user = request.user
    user_questions = Question.objects.filter(author=user).order_by('-created_date')[:10]
    user_answers = Answer.objects.filter(contributor=user).order_by('-created_date')[:10]

    context = {
        'profile_user': user,
        'user_questions': user_questions,
        'user_answers': user_answers,
    }
    return render(request, 'core/profile.html', context)


@login_required
def profile_complete(request):
    """Complete profile with mandatory branch and year."""
    if request.user.is_profile_complete:
        return redirect('home')

    if request.method == 'POST':
        form = ProfileCompleteForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_profile_complete = True
            user.save()
            messages.success(request, 'Profile completed successfully! Welcome to CampusLore.')
            return redirect('home')
    else:
        form = ProfileCompleteForm(instance=request.user)

    return render(request, 'core/profile_complete.html', {'form': form})


@login_required
def question_create(request):
    """Create a new question."""
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            messages.success(request, 'Question posted successfully!')
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm()

    return render(request, 'core/question_form.html', {
        'form': form,
        'is_edit': False,
    })


@login_required
def question_edit(request, pk):
    """Edit a question (author only)."""
    question = get_object_or_404(Question, pk=pk)
    if question.author != request.user:
        return HttpResponseForbidden("You can only edit your own questions.")

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated successfully!')
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm(instance=question)

    return render(request, 'core/question_form.html', {
        'form': form,
        'is_edit': True,
        'question': question,
    })


@login_required
def question_delete(request, pk):
    """Delete a question (author only)."""
    question = get_object_or_404(Question, pk=pk)
    if question.author != request.user:
        return HttpResponseForbidden("You can only delete your own questions.")

    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully.')
        return redirect('question_list')

    return render(request, 'core/confirm_delete.html', {
        'object': question,
        'object_type': 'question',
    })


@login_required
def question_resolve(request, pk):
    """Mark a question as resolved (author only)."""
    question = get_object_or_404(Question, pk=pk)
    if question.author != request.user:
        return HttpResponseForbidden("Only the author can resolve this question.")

    question.status = 'resolved'
    question.save(update_fields=['status'])
    messages.success(request, 'Question marked as resolved!')
    return redirect('question_detail', pk=pk)


@login_required
def answer_create(request, question_pk):
    """Add an answer to a question."""
    question = get_object_or_404(Question, pk=question_pk)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.contributor = request.user
            answer.save()
            messages.success(request, 'Answer posted successfully!')
            return redirect('question_detail', pk=question_pk)

    return redirect('question_detail', pk=question_pk)


@login_required
def answer_edit(request, pk):
    """Edit an answer (contributor only)."""
    answer = get_object_or_404(Answer, pk=pk)
    if answer.contributor != request.user:
        return HttpResponseForbidden("You can only edit your own answers.")

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Answer updated successfully!')
    return redirect('question_detail', pk=answer.question.pk)


@login_required
def answer_delete(request, pk):
    """Delete an answer (contributor only)."""
    answer = get_object_or_404(Answer, pk=pk)
    if answer.contributor != request.user:
        return HttpResponseForbidden("You can only delete your own answers.")

    question_pk = answer.question.pk
    if request.method == 'POST':
        answer.delete()
        messages.success(request, 'Answer deleted successfully.')
    return redirect('question_detail', pk=question_pk)


@login_required
def vote_answer(request, pk):
    """Vote on an answer (AJAX) - helpful or unhelpful."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    answer = get_object_or_404(Answer, pk=pk)
    vote_type = request.POST.get('vote_type')

    if vote_type not in ('helpful', 'unhelpful'):
        return JsonResponse({'error': 'Invalid vote type'}, status=400)

    if answer.contributor == request.user:
        return JsonResponse({'error': 'Cannot vote on your own answer'}, status=403)

    # Toggle: if same vote exists, remove it; if different, change it
    existing_vote = Vote.objects.filter(answer=answer, user=request.user).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Undo the reputation change
            contributor = answer.contributor
            if existing_vote.vote_type == 'helpful':
                contributor.reputation_score = max(0, contributor.reputation_score - 2)
            else:
                contributor.reputation_score += 1
            contributor.save(update_fields=['reputation_score'])
            existing_vote.delete()
            answer.update_counts()
            action = 'removed'
        else:
            # Undo old reputation, apply new
            contributor = answer.contributor
            if existing_vote.vote_type == 'helpful':
                contributor.reputation_score = max(0, contributor.reputation_score - 2)
            else:
                contributor.reputation_score += 1
            contributor.save(update_fields=['reputation_score'])
            existing_vote.vote_type = vote_type
            existing_vote.save()  # This triggers Vote.save() which updates reputation
            action = 'changed'
    else:
        Vote.objects.create(answer=answer, user=request.user, vote_type=vote_type)
        action = 'created'

    answer.refresh_from_db()
    return JsonResponse({
        'helpful_count': answer.helpful_count,
        'action': action,
        'vote_type': vote_type,
    })


@login_required
def confirm_answer(request, pk):
    """Confirm an answer (AJAX)."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    answer = get_object_or_404(Answer, pk=pk)

    if answer.contributor == request.user:
        return JsonResponse({'error': 'Cannot confirm your own answer'}, status=403)

    existing = Confirmation.objects.filter(answer=answer, user=request.user).first()
    if existing:
        # Undo reputation
        contributor = answer.contributor
        contributor.reputation_score = max(0, contributor.reputation_score - 3)
        contributor.save(update_fields=['reputation_score'])
        existing.delete()
        answer.update_counts()
        action = 'removed'
    else:
        Confirmation.objects.create(answer=answer, user=request.user)
        action = 'confirmed'

    answer.refresh_from_db()
    return JsonResponse({
        'confirmation_count': answer.confirmation_count,
        'action': action,
    })


@login_required
def report_content(request, content_type, object_id):
    """Report a question or answer."""
    if content_type == 'question':
        ct = ContentType.objects.get_for_model(Question)
        obj = get_object_or_404(Question, pk=object_id)
    elif content_type == 'answer':
        ct = ContentType.objects.get_for_model(Answer)
        obj = get_object_or_404(Answer, pk=object_id)
    else:
        return HttpResponseForbidden("Invalid content type")

    # Check if already reported by this user
    if Report.objects.filter(
        content_type=ct, object_id=object_id, reporting_user=request.user
    ).exists():
        messages.warning(request, 'You have already reported this content.')
        if content_type == 'question':
            return redirect('question_detail', pk=object_id)
        else:
            return redirect('question_detail', pk=obj.question.pk)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = f"{form.cleaned_data['reason_type']}"
            if form.cleaned_data['details']:
                reason += f": {form.cleaned_data['details']}"

            Report.objects.create(
                content_type=ct,
                object_id=object_id,
                reporting_user=request.user,
                reason=reason,
            )
            messages.success(request, 'Report submitted. Thank you for helping keep CampusLore clean.')
            if content_type == 'question':
                return redirect('question_detail', pk=object_id)
            else:
                return redirect('question_detail', pk=obj.question.pk)
    else:
        form = ReportForm()

    return render(request, 'core/report_form.html', {
        'form': form,
        'reported_object': obj,
        'content_type': content_type,
    })


# ---------------------------------------------------------------------------
# Superuser Views
# ---------------------------------------------------------------------------

@staff_member_required
def admin_reports(request):
    """Admin reports dashboard - superuser only."""
    if not request.user.is_superuser:
        return HttpResponseForbidden("Superuser access required.")

    # Stats
    total_questions = Question.objects.count()
    total_answers = Answer.objects.count()
    total_users = CustomUser.objects.filter(is_profile_complete=True).count()
    total_reports = Report.objects.count()
    pending_reports = Report.objects.filter(status='pending').count()

    # Questions by category
    category_stats = Category.objects.annotate(
        num_questions=Count('questions')
    ).order_by('-num_questions')

    # Activity over last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_questions = Question.objects.filter(created_date__gte=thirty_days_ago).count()
    recent_answers = Answer.objects.filter(created_date__gte=thirty_days_ago).count()

    # Top contributors (by reputation, anonymous)
    top_contributors = CustomUser.objects.filter(
        is_profile_complete=True, reputation_score__gt=0
    ).order_by('-reputation_score')[:10]

    # Pending reports
    pending_report_list = Report.objects.filter(status='pending').select_related(
        'reporting_user', 'content_type'
    )[:20]

    context = {
        'total_questions': total_questions,
        'total_answers': total_answers,
        'total_users': total_users,
        'total_reports': total_reports,
        'pending_reports': pending_reports,
        'category_stats': category_stats,
        'recent_questions': recent_questions,
        'recent_answers': recent_answers,
        'top_contributors': top_contributors,
        'pending_report_list': pending_report_list,
    }
    return render(request, 'core/admin_reports.html', context)


@staff_member_required
def export_csv(request):
    """Export data as CSV - superuser only."""
    if not request.user.is_superuser:
        return HttpResponseForbidden("Superuser access required.")

    report_type = request.GET.get('type', 'questions')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="campuslore_{report_type}.csv"'

    writer = csv.writer(response)

    if report_type == 'questions':
        writer.writerow(['ID', 'Title', 'Category', 'Status', 'Answers', 'Views',
                         'Created Date', 'Anonymous Author'])
        for q in Question.objects.select_related('category').annotate(num_answers=Count('answers')):
            writer.writerow([
                q.id, q.title, q.category.name, q.status,
                q.num_answers, q.view_count,
                q.created_date.strftime('%Y-%m-%d %H:%M'),
                q.anon_display_name,
            ])

    elif report_type == 'activity':
        writer.writerow(['Date', 'Questions Posted', 'Answers Posted'])
        thirty_days_ago = timezone.now() - timedelta(days=30)
        for i in range(30):
            day = thirty_days_ago + timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            q_count = Question.objects.filter(
                created_date__gte=day_start, created_date__lt=day_end
            ).count()
            a_count = Answer.objects.filter(
                created_date__gte=day_start, created_date__lt=day_end
            ).count()
            writer.writerow([day_start.strftime('%Y-%m-%d'), q_count, a_count])

    elif report_type == 'validation':
        writer.writerow(['Answer ID', 'Question', 'Helpful Votes', 'Confirmations',
                         'Anonymous Contributor'])
        for a in Answer.objects.select_related('question'):
            writer.writerow([
                a.id, a.question.title[:80], a.helpful_count,
                a.confirmation_count, a.anon_display_name,
            ])

    return response


@staff_member_required
def export_pdf(request):
    """Export summary report as PDF - superuser only."""
    if not request.user.is_superuser:
        return HttpResponseForbidden("Superuser access required.")

    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("CampusLore - Summary Report", styles['Title']))
    elements.append(Paragraph(
        f"Generated on: {timezone.now().strftime('%Y-%m-%d %H:%M')}",
        styles['Normal']
    ))
    elements.append(Spacer(1, 0.3 * inch))

    # Overview stats
    elements.append(Paragraph("Overview Statistics", styles['Heading2']))
    stats_data = [
        ['Metric', 'Value'],
        ['Total Questions', str(Question.objects.count())],
        ['Total Answers', str(Answer.objects.count())],
        ['Total Users', str(CustomUser.objects.filter(is_profile_complete=True).count())],
        ['Pending Reports', str(Report.objects.filter(status='pending').count())],
    ]
    stats_table = Table(stats_data, colWidths=[3 * inch, 2 * inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#343a40')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Questions by category
    elements.append(Paragraph("Questions by Category", styles['Heading2']))
    cat_data = [['Category', 'Questions']]
    for cat in Category.objects.annotate(num_q=Count('questions')).order_by('-num_q'):
        cat_data.append([cat.name, str(cat.num_q)])

    if len(cat_data) > 1:
        cat_table = Table(cat_data, colWidths=[4 * inch, 1.5 * inch])
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#343a40')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(cat_table)
    else:
        elements.append(Paragraph("No categories yet.", styles['Normal']))

    elements.append(Spacer(1, 0.3 * inch))

    # Top contributors
    elements.append(Paragraph("Top Contributors (Anonymous)", styles['Heading2']))
    top_users = CustomUser.objects.filter(
        reputation_score__gt=0
    ).order_by('-reputation_score')[:10]

    contrib_data = [['Rank', 'Reputation', 'Badge']]
    for i, u in enumerate(top_users, 1):
        contrib_data.append([str(i), str(u.reputation_score), u.badge])

    if len(contrib_data) > 1:
        contrib_table = Table(contrib_data, colWidths=[1 * inch, 2 * inch, 2.5 * inch])
        contrib_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#343a40')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(contrib_table)
    else:
        elements.append(Paragraph("No contributors yet.", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="campuslore_report.pdf"'
    return response
