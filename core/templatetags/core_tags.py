"""
Custom template tags and filters for CampusLore.
"""

from django import template

register = template.Library()


@register.filter
def get_user_vote(answer, user):
    """Get the current user's vote type on an answer, or None."""
    if not user.is_authenticated:
        return None
    vote = answer.votes.filter(user=user).first()
    return vote.vote_type if vote else None


@register.filter
def has_confirmed(answer, user):
    """Check if the current user has confirmed an answer."""
    if not user.is_authenticated:
        return False
    return answer.confirmations.filter(user=user).exists()


@register.filter
def truncate_words_custom(value, num_words):
    """Truncate text to a specified number of words."""
    words = value.split()
    if len(words) > num_words:
        return ' '.join(words[:num_words]) + '...'
    return value
