from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, default='new')
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff', store=True)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], default='north')
    owner_id = fields.Many2one('owner')
    owner_address = fields.Char(related='owner_id.address', readonly=False)
    owner_phone = fields.Char(related='owner_id.phone', readonly=False)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed')
    ], default='draft')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name already exists!')
    ]

    line_ids = fields.One2many('property.line', 'property_id')
    active = fields.Boolean(default=True)

    @api.depends('selling_price', 'expected_price')
    def _compute_diff(self):
        for rec in self:
            print("Inside _compute_diff Method")
            rec.diff = rec.selling_price - rec.expected_price

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            if rec.expected_price < 0:
                return {
                    'warning': {
                        'title': 'Invalid Value',
                        'message': 'Expected price cannot be negative.',
                    }
                }

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Please add a valid number of bedrooms!')

    def action_draft(self):
        for rec in self:
            print("inside draft action")
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            print("inside pending action")
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            print("inside sold action")
            rec.state = 'sold'


    def action_closed(self):
        for rec in self:
            # print("inside closed action")
            rec.state = 'closed'

    def check_expected_selling_date(self):
        # for rec in self: already el elf met handla
        # print(self)
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True

        # rec.state = 'closed'


    # @api.model_create_multi
    # def create(self, vals):
    #     res = super(Property, self).create(vals)
    #     print("inside create method")
    #     return res

    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super(Property, self)._search(domain, offset=0, limit=limit, order=order, access_rights_uid=access_rights_uid)
    #     print("inside search method")
    #     return res

    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     print("inside write method")
    #     return res

    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print("inside unlink method")
    #     return res


class PropertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()
