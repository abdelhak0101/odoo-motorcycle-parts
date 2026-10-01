# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class MotorcycleOrders(models.Model):
    _name = 'mgc.motorcycle.orders'
    _description = 'Motorcycle Parts Management'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('partial', 'Partial payment'),
        ('cancel', 'Cancelled')], default='draft', required=True, string="State")

    customer_id = fields.Many2one('motorcycle.customer', required=True, string="Customer")
    reference = fields.Char(readonly=True)
    product_line_ids = fields.One2many('orders.line', 'order_id', string="Product")
    date = fields.Date(string="Order Date", tracking=50, default=fields.Date.context_today)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    total_price = fields.Monetary(
        compute="_compute_total_price",
        store=True
    )

    payment_method = fields.Selection([
        ('full', 'Full Payment'),
        ('partial', 'Partial Payment')
    ], compute="_compute_payment_method", store=True)
    paid_amount = fields.Monetary(string="Paid Amount", compute="_compute_paid_amount", readonly=False, required=True,
                                  store=True)
    remaining_amount = fields.Monetary(string="Remaining Amount", compute="_compute_remaining_amount", store=True)
    rest_of_paid = fields.Monetary(string='Rest Paid', compute="_compute_rest_paid", store=True)

    def action_paid(self):
        for rec in self:

            invalid_lines = rec.product_line_ids.filtered(
                lambda l: l.qty > l.product_id.quantity
            )

            if invalid_lines:
                products = ', '.join(invalid_lines.mapped('product_id.name'))

                raise ValidationError(
                    f'Insufficient quantity for: {products}'
                )

            if rec.payment_method == 'partial':
                raise ValidationError(
                    'You cannot mark this order as paid because the payment method is partial.'
                )

            if rec.paid_amount > rec.total_price:
                rec.customer_id.old_remaining_amount = (rec.customer_id.old_remaining_amount - rec.rest_of_paid)


            for line in rec.product_line_ids:
                line.product_id.quantity -= line.qty

            rec.state = 'paid'

    def action_remaining_paid(self):
        self.ensure_one()

        # check stock before anything
        invalid_lines = self.product_line_ids.filtered(
            lambda l: l.qty > l.product_id.quantity
        )

        if invalid_lines:
            products = ', '.join(
                invalid_lines.mapped('product_id.name')
            )

            raise ValidationError(
                f'Insufficient quantity for: {products}'
            )

        # partial payment wizard
        if self.payment_method == 'partial' and self.paid_amount <= 0:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Confirmation',
                'res_model': 'payment.confirm.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_order_id': self.id,
                }
            }

        # reduce stock
        for line in self.product_line_ids:
            line.product_id.quantity = (
                    line.product_id.quantity - line.qty
            )

        self.state = 'partial'

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code('motorcycle.order')
        return super(MotorcycleOrders, self).create(vals)

    @api.depends('product_line_ids.price_subtotal')
    def _compute_total_price(self):
        for order in self:
            order.total_price = sum(
                order.product_line_ids.mapped('price_subtotal')
            )

    @api.depends('total_price', 'paid_amount')
    def _compute_remaining_amount(self):
        for order in self:
            if order.paid_amount > order.total_price:
                order.remaining_amount = 0
            else:
                order.remaining_amount = (order.total_price - order.paid_amount)

    @api.depends('total_price', 'payment_method')
    def _compute_paid_amount(self):
        for order in self:
            if order.payment_method == 'full':
                order.paid_amount = order.total_price

    @api.depends('total_price', 'paid_amount')
    def _compute_rest_paid(self):
        for order in self:
            order.rest_of_paid = max(
                (order.paid_amount or 0.0) - (order.total_price or 0.0),
                0.0
            )

    @api.depends('total_price', 'paid_amount')
    def _compute_payment_method(self):
        for order in self:
            order.payment_method = (
                'full'
                if (order.paid_amount or 0.0) >= (order.total_price or 0.0)
                else 'partial'
            )


class OrdersLine(models.Model):
    _name = 'orders.line'

    order_id = fields.Many2one(
        'mgc.motorcycle.orders',
        string="Order",
        ondelete='cascade'
    )
    product_id = fields.Many2one(
        'motorcycle.product.template',
        string="Product",
        required=True
    )
    qty = fields.Float(string="Quantity", default=1)
    price_unit = fields.Monetary(string="Unit Price", related="product_id.whole_sale_price", store=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='order_id.currency_id', store=True)
    price_subtotal = fields.Monetary(string="Subtotal", compute='_compute_price_subtotal', store=True)

    insufficient_qty = fields.Boolean(
        compute='_compute_insufficient_qty',
        store=False
    )

    @api.depends('qty', 'product_id.quantity')
    def _compute_insufficient_qty(self):
        for line in self:
            line.insufficient_qty = line.qty > line.product_id.quantity

    @api.constrains('qty', 'product_id')
    def _check_quantity(self):
        for line in self:

            if line.qty > line.product_id.quantity:
                raise ValidationError(
                    f'Insufficient quantity for {line.product_id.name}'
                )

    @api.depends('price_unit', 'qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty
