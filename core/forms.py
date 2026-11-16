"""
Django forms for CampusLore.
"""

from django import forms
from .models import Question, Answer, Report, CustomUser
from .college_data import BRANCH_CHOICES, YEAR_CHOICES


class ProfileCompleteForm(forms.ModelForm):
    """Form for completing user profile after first Google login."""
    branch = forms.ChoiceField(
        choices=[('', '-- Select Branch --')] + BRANCH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    year = forms.ChoiceField(
        choices=[('', '-- Select Year --')] + [(str(k), v) for k, v in YEAR_CHOICES],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = CustomUser
        fields = ['branch', 'year']

    def clean_year(self):
        return int(self.cleaned_data['year'])


class QuestionForm(forms.ModelForm):
    """Form for creating / editing a question."""

    class Meta:
        model = Question
        fields = ['title', 'description', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your question title...',
                'id': 'question-title-input',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your question in detail...',
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. exam, semester-5, java (comma-separated)',
            }),
        }


class AnswerForm(forms.ModelForm):
    """Form for adding / editing an answer."""

    class Meta:
        model = Answer
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your answer here...',
            }),
        }


class ReportForm(forms.Form):
    """Form for reporting inappropriate content."""
    REASON_CHOICES = [
        ('spam', 'Spam or advertising'),
        ('offensive', 'Offensive or inappropriate content'),
        ('misleading', 'Misleading or false information'),
        ('duplicate', 'Duplicate content'),
        ('other', 'Other'),
    ]
    reason_type = forms.ChoiceField(
        choices=REASON_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    details = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Provide additional details...',
        }),
        required=False,
    )
