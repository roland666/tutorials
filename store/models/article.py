from odoo import models, fields, api


class Article(models.Model):
    _name = "store.article"
    _description = "Article"

    name = fields.Char(string="Name", required=True)
    stock_quantity = fields.Integer(string="Stock Quantity", default=0)
    price = fields.Float(string="Price")
    discount = fields.Float(string="Discount (%)", default=0.0)
    discounted_price = fields.Float(string="Discounted Price", compute="_compute_discounted_price", store=True)
    serial_number = fields.Char(string="Serial Number")
    warranty_period = fields.Integer(string="Warranty (months)", default=0)
    description = fields.Text(string="Description")

    category_ids = fields.Many2many(
        comodel_name="store.category",
        string="Categories",
        required=True)

    _sql_constraints = [
        ('unique_serial_number', 'unique(serial_number)', 'The serial number must be unique.')
    ]

    @api.depends('price', 'discount')
    def _compute_discounted_price(self):
        for record in self:
            if record.discount:
                record.discounted_price = record.price * (1 - record.discount / 100)
            else:
                record.discounted_price = record.price

    def action_create_order(self):
        self.ensure_one()
        return {
            'name': 'Create Order',
            'type': 'ir.actions.act_window',
            'res_model': 'store.order',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_article_id': self.id,
                'default_price': self.discounted_price,
            }
        }
