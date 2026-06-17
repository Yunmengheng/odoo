from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class LibrarySlip(models.Model):
    _name = 'library.slip'
    _description = 'Borrowing Slip'
    _order = 'name desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    student_id = fields.Many2one('library.student', string='Student', required=True)
    book_id = fields.Many2one('library.book', string='Book', required=True, domain="[('state', '=', 'available')]")
    borrowed_date = fields.Date(string='Borrowed Date', default=fields.Date.today, required=True)
    return_date = fields.Date(string='Return Date', compute='_compute_return_date', store=True)
    actual_return_date = fields.Date(string='Actual Return Date', readonly=True)
    state = fields.Selection([
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
    ], string='Status', default='borrowed', copy=False, tracking=True)

    @api.depends('borrowed_date')
    def _compute_return_date(self):
        for slip in self:
            if slip.borrowed_date:
                slip.return_date = slip.borrowed_date + timedelta(days=7)
            else:
                slip.return_date = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('library.slip') or _('New')
            
            # Check if book is available
            book = self.env['library.book'].browse(vals.get('book_id'))
            if book.state != 'available':
                raise ValidationError(_("The book '%s' is already borrowed.") % book.name)
            
            book.state = 'borrowed'
        return super(LibrarySlip, self).create(vals_list)

    def action_return_book(self):
        for slip in self:
            if slip.state == 'borrowed':
                slip.write({
                    'state': 'returned',
                    'actual_return_date': fields.Date.today(),
                })
                slip.book_id.state = 'available'

    @api.constrains('book_id', 'state')
    def _check_book_availability(self):
        for record in self:
            if record.state == 'borrowed':
                # Check if another active slip exists for the same book
                domain = [
                    ('id', '!=', record.id),
                    ('book_id', '=', record.book_id.id),
                    ('state', '=', 'borrowed'),
                ]
                if self.search_count(domain) > 0:
                    raise ValidationError(_("This book is already borrowed by someone else."))
