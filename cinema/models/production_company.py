from odoo import fields, models


class ProductionCompany(models.Model):
    _name = "cinema.production.company"
    _description = "Production Company"

    name = fields.Char(
        required=True,
        string="Name"
    )

    _sql_constraints = [
        ('production_company_check_name_unique', 'UNIQUE(name)', 'The name of the production company must be unique.')
    ]
