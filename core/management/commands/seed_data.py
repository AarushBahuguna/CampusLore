"""
Management command to seed initial categories and programs.
"""

from django.core.management.base import BaseCommand
from core.models import Category, Program


INITIAL_CATEGORIES = [
    ('Courses & Subjects', 'Questions about courses, subjects, curriculum, and syllabus.'),
    ('Professors', 'Questions and reviews about professors and teaching staff.'),
    ('Exams & Assignments', 'Questions about exams, assignments, grading, and evaluations.'),
    ('Internships & Placements', 'Questions about internships, placements, companies, and career.'),
    ('Clubs & Societies', 'Questions about student clubs, societies, and extracurricular activities.'),
    ('Hostel / Campus Facilities', 'Questions about hostel life, mess, campus facilities.'),
    ('Events', 'Questions about college events, fests, workshops, and seminars.'),
    ('Administrative Procedures', 'Questions about admissions, fees, documents, and administrative processes.'),
    ('Study Resources', 'Questions about study materials, books, notes, and online resources.'),
    ('General Campus Queries', 'General questions about campus life, tips, and miscellaneous topics.'),
]

INITIAL_PROGRAMS = [
    ('B.Tech Computer Science & Engineering', 'CSE', 'CSE/IT', 4),
    ('B.Tech Information Technology', 'IT', 'CSE/IT', 4),
    ('B.Tech Electronics & Communication Engineering', 'ECE', 'ECE & MED', 4),
    ('B.Tech Biotechnology', 'BT', 'Biotechnology & Chemistry', 4),
    ('MCA - Master of Computer Applications', 'MCA', 'Computer Applications', 3),
    ('MBA - Master of Business Administration', 'MBA', 'Jaypee Business School', 2),
]


class Command(BaseCommand):
    help = 'Seed initial categories and programs for CampusLore'

    def handle(self, *args, **options):
        self.stdout.write('Seeding categories...')
        for name, desc in INITIAL_CATEGORIES:
            cat, created = Category.objects.get_or_create(
                name=name, defaults={'description': desc}
            )
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f'  {status}: {name}')

        self.stdout.write('\nSeeding programs...')
        for name, short, dept, duration in INITIAL_PROGRAMS:
            prog, created = Program.objects.get_or_create(
                name=name,
                defaults={
                    'short_name': short,
                    'department': dept,
                    'duration_years': duration,
                }
            )
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f'  {status}: {name}')

        self.stdout.write(self.style.SUCCESS('\nSeeding complete!'))
