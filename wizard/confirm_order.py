import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta
from datetime import date


class PaymentConfirmWizard(models.TransientModel):
    _name = "payment.confirm.wizard"
    _description = "Payment Confirm Wizard"

    order_id = fields.Many2one('mgc.motorcycle.orders')

    def action_confirm(self):
        self.order_id.state = 'partial'