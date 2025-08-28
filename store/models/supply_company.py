from odoo import models, fields


class SupplyCompany(models.Model):
    _name = "store.supply.company"
    _description = "Supply Company"

    name = fields.Char(string="Name", required=True)
    contact_name = fields.Char(string="Contact Name")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    supply_company_rating = fields.Selection([
        ('A', 'A - Excellent'),
        ('B', 'B - Good'),
        ('C', 'C - Average'),
        ('D', 'D - Poor'),
        ('N', 'N - Not Rated Yet')
    ], string="Supply Company Rating", default='N')

    order_ids = fields.One2many(
        comodel_name="store.order",
        inverse_name="supply_company_id",
        string="Orders"
    )

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The supply company name must be unique.')
    ]
