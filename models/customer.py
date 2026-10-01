# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MotorcycleCustomer(models.Model):
    _name = 'motorcycle.customer'
    _description = 'Motorcycle Customer'

    name = fields.Char(required=True)

    phone = fields.Char()
    email = fields.Char()
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)
    address = fields.Text()
    image = fields.Image(string="")


    customer_type = fields.Selection([
        ('wholesale', 'Wholesale'),
        ('retail', 'Retail'),
    ], default='wholesale')

    order_ids = fields.One2many('mgc.motorcycle.orders', 'customer_id', string="Orders")

    old_remaining_amount = fields.Monetary(string="Old Remaining Amount",
                                           help="Manual starting debt or initial remaining amount", store=True)
    order_remaining_amount = fields.Monetary(string="Orders Remaining Amount",
                                             compute="_compute_order_remaining_amount", store=True)
    all_remaining_amount = fields.Monetary(string="All Remaining Amount", compute="_compute_all_remaining_amount",
                                           store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    @api.depends('order_ids.remaining_amount')
    def _compute_order_remaining_amount(self):
        for customer in self:
            customer.order_remaining_amount = sum(
                customer.order_ids.mapped('remaining_amount')
            )

    @api.depends('order_ids', 'order_ids.remaining_amount', 'old_remaining_amount')
    def _compute_all_remaining_amount(self):
        for customer in self:
            customer.all_remaining_amount = (
                    sum(customer.order_ids.mapped('remaining_amount')) +
                    (customer.old_remaining_amount or 0.0)
            )
