from odoo import models, fields, api


class Category(models.Model):
    _name = "store.category"
    _description = "Category"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")

    article_ids = fields.Many2many(
        comodel_name="store.article",
        inverse_name="category_ids",
        string="Articles",
        compute="_compute_article_ids"
    )

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The category name must be unique.')
    ]

    def _compute_article_ids(self):
        print("DEBUG : _compute_article_ids called")
        for cat in self:
            cat.article_ids = self.env['store.article'].search([('category_ids', 'in', cat.id)])
