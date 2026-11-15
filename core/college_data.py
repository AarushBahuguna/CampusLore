"""
Hardcoded JIIT college information.
"""

COLLEGE_INFO = {
    'name': 'Jaypee Institute of Information Technology',
    'short_name': 'JIIT',
    'website': 'https://www.jiit.ac.in/',
    'webportal': 'https://webportal.jiit.ac.in/jiitwebkiosk/',
    'campuses': [
        {
            'name': 'Sector 62 Campus',
            'address': 'A-10, Sector-62, Noida-201 309, Uttar Pradesh, India',
            'phone': '+91-9999912862, 9999962128',
            'email': 'admission@mail.jiit.ac.in',
        },
        {
            'name': 'Sector 128 Campus',
            'address': 'Sector-128, Jaypee Wish Town Village, Sultanpur, Noida-201 304, Uttar Pradesh, India',
            'phone': '0120-4195808/809',
            'email': None,
        },
    ],
    'leadership': [
        {'name': 'Shri. Manoj Gaur', 'designation': 'Chancellor'},
        {'name': 'Prof. (Dr.) S C Saxena', 'designation': 'Pro-Chancellor'},
        {'name': 'Prof. (Dr.) Rajive Kumar', 'designation': 'Vice-Chancellor'},
        {'name': 'Col (Dr) Sharad Rastogi', 'designation': 'Registrar', 'email': 'registrar@jiit.ac.in'},
    ],
    'departments': [
        {
            'name': 'Computer Science & Engineering / Information Technology',
            'hod': 'Prof. Vikas Saxena',
            'designation': 'Director & HoD - CSE/IT',
            'ext': '247',
            'email': 'vikas.saxena@mail.jiit.ac.in',
        },
        {
            'name': 'Mathematics',
            'hod': 'Prof. Alka Tripathi',
            'designation': 'HoD - Mathematics',
            'ext': '341',
            'email': 'alka.choubey@mail.jiit.ac.in',
        },
        {
            'name': 'Biotechnology & Chemistry',
            'hod': 'Prof. Pammi Gauba',
            'designation': 'Dean (A&R)-I and HoD - Biotechnology & Chemistry',
            'ext': '343',
            'email': 'pammi.gauba@mail.jiit.ac.in',
        },
        {
            'name': 'Humanities & Social Sciences',
            'hod': 'Prof. Monika Suri',
            'designation': 'Dean & HoD - HSS',
            'ext': '380',
            'email': 'monika.suri@mail.jiit.ac.in',
        },
        {
            'name': 'Electronics & Communication Engineering / Mechanical Engineering Design',
            'hod': 'Prof. Shweta Srivastava',
            'designation': 'Dean (A&R)-II and HoD - ECE & MED',
            'ext': '319',
            'email': 'shweta.srivastava@mail.jiit.ac.in',
        },
        {
            'name': 'Physics, Materials Science & Engineering',
            'hod': 'Prof. Anirban Pathak',
            'designation': 'HoD - PMSE',
            'ext': '361',
            'email': 'anirban.pathak@mail.jiit.ac.in',
        },
        {
            'name': 'Computer Applications',
            'hod': 'Prof. Sandeep Kumar Singh',
            'designation': 'HoD - Computer Applications',
            'ext': '259',
            'email': 'sandeepk.singh@mail.jiit.ac.in',
        },
        {
            'name': 'Jaypee Business School',
            'hod': 'Prof. Anubha Vashisht',
            'designation': 'Director - JBS',
            'ext': '483',
            'email': 'anubha.vashisht@mail.jiit.ac.in',
        },
    ],
}

# Branch choices for student profiles
BRANCH_CHOICES = [
    ('CSE', 'Computer Science & Engineering'),
    ('IT', 'Information Technology'),
    ('ECE', 'Electronics & Communication Engineering'),
    ('BT', 'Biotechnology'),
    ('MCA', 'Master of Computer Applications'),
    ('MBA', 'Master of Business Administration'),
    ('OTHER', 'Other'),
]

# Year choices
YEAR_CHOICES = [
    (1, '1st Year'),
    (2, '2nd Year'),
    (3, '3rd Year'),
    (4, '4th Year'),
    (5, '5th Year'),
]
