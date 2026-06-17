from odoo import models, fields, api

class AddBookWizard(models.TransientModel):
    _name = 'library.book.wizard'
    _description = 'Add New Book Wizard'

    name = fields.Char(string='Book Title', required=True)
    author = fields.Char(string='Author', required=True)
    isbn = fields.Char(string='ISBN')
    description = fields.Text(string='Description')

    def action_create_book(self):
        self.env['library.book'].create({
            'name': self.name,
            'author': self.author,
            'isbn': self.isbn,
            'description': self.description,
        })
        return {'type': 'ir.actions.act_window_close'}
