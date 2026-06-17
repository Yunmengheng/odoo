from odoo import models, fields, api

class AddStudentWizard(models.TransientModel):
    _name = 'library.student.wizard'
    _description = 'Add New Student Wizard'

    name = fields.Char(string='Name', required=True)
    student_id = fields.Char(string='Student ID', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')

    def action_create_student(self):
        self.env['library.student'].create({
            'name': self.name,
            'student_id': self.student_id,
            'email': self.email,
            'phone': self.phone,
        })
        return {'type': 'ir.actions.act_window_close'}
