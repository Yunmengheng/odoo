from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LibraryStudent(models.Model):
    _name = 'library.student'
    _description = 'Library Student'

    name = fields.Char(string='Name', required=True)
    student_id = fields.Char(string='Student ID', required=True, copy=False)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    borrow_slip_ids = fields.One2many('library.slip', 'student_id', string='Borrow Slips')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('student_id_unique', 'unique(student_id)', 'The Student ID must be unique!')
    ]

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError(_("The student name cannot be empty."))
