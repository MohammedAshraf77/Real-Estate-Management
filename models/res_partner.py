from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_id = fields.Many2one('property', string="Property")
     # price = fields.Float(related='property_id.selling_price') this is the best way to use by attribute related
    price = fields.Float(string="Price", compute='_compute_price')

    @api.depends('property_id.selling_price')
    def _compute_price(self):
        for rec in self:
            if rec.property_id:  #   A MAKE SHURE EN PROPERTY ID MAWGOOD
                rec.price = rec.property_id.selling_price
            else:
                rec.price = 0.0
