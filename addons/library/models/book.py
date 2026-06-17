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
        
        # Link current user to student record via user_id
        student = self.env['library.student'].search([('user_id', '=', self.env.user.id)], limit=1)
        if not student:
             raise ValidationError(_("You are not linked to a student record. Please contact the librarian to link your user account."))
        
        # Use sudo to allow updating the state even if the student doesn't have write access
        self.sudo().write({'state': 'borrowed'})
        
        self.env['library.slip'].sudo().create({
            'student_id': student.id,
            'book_id': self.id,
            'borrowed_date': fields.Date.today(),
        })

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError(_("The book title cannot be empty."))
