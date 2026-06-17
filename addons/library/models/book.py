from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Book Title', required=True)
    author = fields.Char(string='Author', required=True)
    isbn = fields.Char(string='ISBN')
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    ], string='Status', default='available', copy=False, tracking=True)
    borrow_count = fields.Integer(string='Borrow Count', compute='_compute_borrow_count', store=True)
    active = fields.Boolean(string='Active', default=True)

    @api.depends('slip_ids')
    def _compute_borrow_count(self):
        for book in self:
            book.borrow_count = len(book.slip_ids)

    slip_ids = fields.One2many('library.slip', 'book_id', string='Borrow Slips')

    def action_borrow_book(self):
        self.ensure_one()
        if self.state != 'available':
            raise ValidationError(_("This book is already borrowed."))
        
        # Get current student based on user (assuming user maps to student)
        # For this implementation, we will raise an error if no student is found
        student = self.env['library.student'].search([('name', '=', self.env.user.name)], limit=1)
        if not student:
             # Fallback: prompt to link student or create slip manually if needed
             raise ValidationError(_("You are not linked to a student record. Please contact the librarian."))
        
        self.env['library.slip'].create({
            'student_id': student.id,
            'book_id': self.id,
            'borrowed_date': fields.Date.today(),
        })

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError(_("The book title cannot be empty."))
