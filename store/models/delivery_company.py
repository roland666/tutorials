from odoo import models, fields


class DeliveryCompany(models.Model):
    _name = "store.delivery.company"
    _description = "Delivery company"

    name = fields.Char(string="Name", required=True)
    contact_name = fields.Char(string="Contact Name")
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    usual_delivery_time = fields.Integer(string="Usual Delivery Time (days)", default=3)
    delivery_rating = fields.Selection([
        ('A', 'A - Excellent'),
        ('B', 'B - Good'),
        ('C', 'C - Average'),
        ('D', 'D - Poor'),
        ('N', 'N - Not Rated Yet')
    ], string="Delivery Rating", default='N')

    order_ids = fields.One2many(
        comodel_name="store.order",
        inverse_name="delivery_company_id",
        string="Orders"
    )

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The delivery company name must be unique.')
    ]

    def write(self, vals):
        res = super().write(vals)
        if "usual_delivery_time" in vals:
            for company in self:
                company.order_ids._compute_expected_delivery_date()
        return res
