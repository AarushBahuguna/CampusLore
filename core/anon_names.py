"""
Anonymous display name generator.
Generates names in the format: JIITIAN<random-number>
"""

import random
from django.db.models import Q


def generate_anon_name(model_class=None, field_name='anon_display_name'):
    """
    Generate a unique anonymous display name in the format JIITIAN<4-digit-number>.
    If model_class is provided, ensures uniqueness against existing records.
    """
    max_attempts = 100
    for _ in range(max_attempts):
        number = random.randint(1000, 9999)
        name = f"JIITIAN{number}"
        if model_class is None:
            return name
        # Check uniqueness
        if not model_class.objects.filter(**{field_name: name}).exists():
            return name
    # Fallback: use larger range
    number = random.randint(10000, 99999)
    return f"JIITIAN{number}"
