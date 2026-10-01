# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _name = 'motorcycle.product.template'
    _description = 'Product Template'

    name = fields.Char(required=True)
    reference = fields.Char(string="Internal Reference", readonly=True)

    price = fields.Monetary(string="Sale Price")
    whole_sale_price = fields.Monetary(string="Wholesale Price")
    cost = fields.Monetary(string="Cost")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    quantity = fields.Float(string="On Hand Quantity")
    product_type = fields.Selection([('gy6', 'Gy6'), ('cg', 'Cg'), ('sym', 'SYM'), ('110', '110')],
                                    string="Product Type")

    active = fields.Boolean(default=True)
    image = fields.Image(string="")
    barcode = fields.Char(string="Barcode" , readonly=True)
    _sql_constraints = [
        ('barcode_unique', 'unique(barcode)', 'Barcode must be unique!')
    ]

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code('motorcycle.products')
        vals['barcode'] = self.env['ir.sequence'].next_by_code('motorcycle.barcode')
        return super(ProductTemplate, self).create(vals)

    def write(self, vals):
        for record in self:
            new_vals = dict(vals)
            if not record.reference and not vals.get('reference'):
                new_vals['reference'] = self.env['ir.sequence'].next_by_code(
                    'editable.motorcycle.products'
                )
            if not record.barcode and not vals.get('barcode'):
                new_vals['barcode'] = self.env['ir.sequence'].next_by_code(
                    'editable.motorcycle.barcode'
                )
            super(ProductTemplate, record).write(new_vals)
        return True

