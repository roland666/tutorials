from odoo import models, fields, api
from datetime import timedelta


class Order(models.Model):
    _name = "store.order"
    _description = "Order"

    number = fields.Char(string="Order Number", readonly=True, default=lambda self: 'New Order')
    order_date = fields.Datetime(string="Order Date", required=True, default=fields.Datetime.now, readonly=True)
    total_amount = fields.Float(string="Total Amount", required=True)
    tracking_url = fields.Char(string="Tracking URL")
    expected_delivery_date = fields.Date(string="Expected Delivery Date", compute="_compute_expected_delivery_date", store=True)
    delivery_date = fields.Datetime(string="Delivery Date")
    notes = fields.Text(string="Notes")
    delivery_status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled')
    ], string="Delivery Status", default='pending')

    article_id = fields.Many2one(
        comodel_name="store.article",
        string="Article",
        required=True)
    supply_company_id = fields.Many2one(
        comodel_name="store.supply.company",
        string="Supply Company",
        required=True)
    delivery_company_id = fields.Many2one(
        comodel_name="store.delivery.company",
        string="Delivery Company")

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record.number = str(record.id)
        return record

    @api.depends('delivery_company_id', 'order_date')
    def _compute_expected_delivery_date(self):
        for order in self:
            order.expected_delivery_date = order.order_date.date() + timedelta(days=order.delivery_company_id.usual_delivery_time)
