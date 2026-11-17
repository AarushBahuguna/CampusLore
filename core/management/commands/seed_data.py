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
    ('B.Tech - Artificial Intelligence and Machine Learning (AI & ML)', 'AI & ML', 'Computer Science & Engineering / IT', 120, 4),
    ('B.Tech - Biotechnology', 'BT', 'Biotechnology & Chemistry', 120, 4),
    ('B.Tech - Computer Science & Engineering (CSE)', 'CSE', 'Computer Science & Engineering', 1140, 4),
    ('B.Tech - Computer Science & Engineering (Cyber Security)', 'Cyber Security', 'Computer Science & Engineering', 60, 4),
    ('B.Tech - Electronics & Communication Engineering (ECE)', 'ECE', 'Electronics & Communication Engineering', 240, 4),
    ('B.Tech - Electronics & Communication Engineering (Advanced Communication Technology)', 'Advanced Communication', 'Electronics & Communication Engineering', 60, 4),
    ('B.Tech - Electronics and Computer Engineering (ECM)', 'ECM', 'Electronics & Communication Engineering', 60, 4),
    ('B.Tech - Electronics Engineering (VLSI Design and Technology)', 'VLSI', 'Electronics & Communication Engineering', 60, 4),
    ('B.Tech - Information Technology (IT)', 'IT', 'Computer Science & Engineering / IT', 180, 4),
    ('B.Tech - Mathematics and Computing (M&C)', 'M&C', 'Mathematics', 120, 4),
    ('B.Tech - Robotics and Artificial Intelligence (R & A)', 'R & A', 'Computer Science & Engineering / IT', 30, 4),
    ('Integrated M.Tech - Biotechnology', 'Int. M.Tech BT', 'Biotechnology & Chemistry', 30, 5),
    ('Integrated M.Tech - Computer Science & Engineering (CSE)', 'Int. M.Tech CSE', 'Computer Science & Engineering', 30, 5),
    ('Integrated M.Tech - Electronics & Communication Engineering (ECE)', 'Int. M.Tech ECE', 'Electronics & Communication Engineering', 30, 5),
    ('Integrated M.Tech - Artificial Intelligence and Data Science (AI & DS)', 'Int. M.Tech AI & DS', 'Computer Science & Engineering / IT', 30, 5),
    ('M.Tech - Biotechnology', 'M.Tech BT', 'Biotechnology & Chemistry', 18, 2),
    ('M.Tech - Computer Science & Engineering (CSE)', 'M.Tech CSE', 'Computer Science & Engineering', 30, 2),
    ('M.Tech - Quantum Technology', 'M.Tech QT', 'Physics / Electronics', 12, 2),
    ('M.Tech - Robotics and Artificial Intelligence (R & A)', 'M.Tech R & A', 'Computer Science & Engineering / IT', 12, 2),
    ('M.Tech - VLSI Design', 'M.Tech VLSI', 'Electronics & Communication Engineering', 12, 2),
    ('M.Sc - Artificial Intelligence and Machine Learning (AI & ML)', 'M.Sc AI & ML', 'Mathematics / Computer Science', 15, 2),
    ('M.Sc - Bioinformatics', 'M.Sc Bioinformatics', 'Biotechnology & Chemistry', 30, 2),
    ('M.Sc - Cyber Security', 'M.Sc Cyber Security', 'Computer Science & Engineering', 15, 2),
    ('M.Sc - Mathematics', 'M.Sc Mathematics', 'Mathematics', 10, 2),
    ('M.Sc - Microbiology', 'M.Sc Microbiology', 'Biotechnology & Chemistry', 10, 2),
    ('M.Sc - Physics', 'M.Sc Physics', 'Physics', 60, 2),
    ('B.Sc - Computer Science (CS)', 'B.Sc CS', 'Computer Science', 10, 4),
    ('B.Sc - Forensic Science', 'B.Sc Forensic Science', 'Forensic Science', 30, 4),
    ('BCA - Bachelor of Computer Applications', 'BCA', 'Computer Applications', 15, 4),
    ('BBA - Bachelor of Business Administration', 'BBA', 'Jaypee Business School', 120, 4),
    ('B.Com - Bachelor of Commerce', 'B.Com', 'Jaypee Business School', 120, 4),
    ('MBA - Master of Business Administration', 'MBA', 'Jaypee Business School', 60, 2),
    ('MCA - Master of Computer Applications', 'MCA', 'Computer Applications', 30, 2),
    ('M.Des - Master of Design', 'M.Des', 'All Departments', 30, 2),
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
        for name, short, dept, batch_size, duration in INITIAL_PROGRAMS:
            prog, created = Program.objects.get_or_create(
                name=name,
                defaults={
                    'short_name': short,
                    'department': dept,
                    'batch_size': batch_size,
                    'duration_years': duration,
                }
            )
            if not created:
                prog.short_name = short
                prog.department = dept
                prog.batch_size = batch_size
                prog.duration_years = duration
                prog.save(update_fields=['short_name', 'department', 'batch_size', 'duration_years'])
            status = 'Created' if created else 'Updated'
            self.stdout.write(f'  {status}: {name}')

        self.stdout.write(self.style.SUCCESS('\nSeeding complete!'))
