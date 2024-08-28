from odoo import models, fields

class Building(models.Model):
    _name = 'building'
    _description = 'Building Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'code'

    no = fields.Integer()
    name = fields.Char()
    code = fields.Char()
    description = fields.Text()
    active = fields.Boolean(default=True)


