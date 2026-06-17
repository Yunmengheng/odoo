{
    'name': 'Library Management System',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Manage books and students borrowing books',
    'description': """
        Library Management System for Odoo 18.
        Features:
        - Book management
        - Student management
        - Borrowing slips management
    """,
    'author': 'Gemini CLI',
    'depends': ['base'],
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/book_views.xml',
        'views/student_views.xml',
        'views/slip_views.xml',
        'views/wizard_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
