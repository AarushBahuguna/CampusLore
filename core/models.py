"""
Core models for CampusLore.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .college_data import BRANCH_CHOICES, YEAR_CHOICES
from .anon_names import generate_anon_name


class CustomUser(AbstractUser):
    """Custom user model for CampusLore students."""
    college_email = models.EmailField(unique=True, blank=True, null=True)
    branch = models.CharField(max_length=25, choices=BRANCH_CHOICES, blank=True)
    year = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True)
    account_status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('suspended', 'Suspended'), ('banned', 'Banned')],
        default='active',
    )
    reputation_score = models.IntegerField(default=0)
    is_profile_complete = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.college_email or self.username

    @property
    def badge(self):
        """Return a badge based on reputation score."""
        if self.reputation_score >= 100:
            return 'Trusted Voice'
        elif self.reputation_score >= 50:
            return 'Helpful Contributor'
        elif self.reputation_score >= 20:
            return 'Active Member'
        elif self.reputation_score >= 5:
            return 'Newcomer'
        return 'New JIITian'


class Category(models.Model):
    """Categories for organizing questions."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Bootstrap icon class')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def question_count(self):
        return self.questions.count()


class Question(models.Model):
    """A question posted by a student."""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='questions'
    )
    anon_display_name = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.anon_display_name:
            self.anon_display_name = generate_anon_name(Question)
        super().save(*args, **kwargs)

    @property
    def answer_count(self):
        return self.answers.count()

    @property
    def tag_list(self):
        """Return tags as a list."""
        if self.tags:
            return [t.strip() for t in self.tags.split(',') if t.strip()]
        return []

    @property
    def total_votes(self):
        """Total helpful votes across all answers."""
        return sum(a.helpful_count for a in self.answers.all())


class Answer(models.Model):
    """An answer to a question."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    description = models.TextField()
    contributor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='answers'
    )
    anon_display_name = models.CharField(max_length=50, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    helpful_count = models.IntegerField(default=0)
    confirmation_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-helpful_count', '-confirmation_count', '-created_date']

    def __str__(self):
        return f"Answer to: {self.question.title[:50]}"

    def save(self, *args, **kwargs):
        if not self.anon_display_name:
            self.anon_display_name = generate_anon_name(Answer)
        super().save(*args, **kwargs)

    def update_counts(self):
        """Recalculate vote and confirmation counts."""
        self.helpful_count = self.votes.filter(vote_type='helpful').count()
        unhelpful = self.votes.filter(vote_type='unhelpful').count()
        self.helpful_count = self.helpful_count - unhelpful
        self.confirmation_count = self.confirmations.count()
        self.save(update_fields=['helpful_count', 'confirmation_count'])


class Vote(models.Model):
    """A vote on an answer (helpful or unhelpful)."""
    VOTE_TYPES = [
        ('helpful', 'Helpful'),
        ('unhelpful', 'Unhelpful'),
    ]

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('answer', 'user')

    def __str__(self):
        return f"{self.vote_type} on Answer #{self.answer.id} by User #{self.user.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.answer.update_counts()
        # Update contributor reputation
        contributor = self.answer.contributor
        if self.vote_type == 'helpful':
            contributor.reputation_score += 2
        else:
            contributor.reputation_score = max(0, contributor.reputation_score - 1)
        contributor.save(update_fields=['reputation_score'])


class Confirmation(models.Model):
    """A confirmation that an answer is accurate based on shared experience."""
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='confirmations')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='confirmations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('answer', 'user')

    def __str__(self):
        return f"Confirmation on Answer #{self.answer.id} by User #{self.user.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.answer.update_counts()
        # Boost contributor reputation for confirmations
        contributor = self.answer.contributor
        contributor.reputation_score += 3
        contributor.save(update_fields=['reputation_score'])


class Report(models.Model):
    """A report on inappropriate content (question or answer)."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]

    # Generic relation to allow reporting both Questions and Answers
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    reported_item = GenericForeignKey('content_type', 'object_id')

    reporting_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reports_made'
    )
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Report #{self.id} - {self.status}"


class Program(models.Model):
    """Academic programs offered at JIIT (placeholder for batch size data)."""
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=200, blank=True)
    batch_size = models.PositiveIntegerField(null=True, blank=True, help_text='To be updated')
    duration_years = models.PositiveIntegerField(default=4)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
