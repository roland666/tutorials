from odoo import fields, models


class Genre(models.Model):
    _name = "cinema.genre"
    _description = "Genre"

    name = fields.Char(
        string="Name",
        required=True
    )

    _sql_constraints = [
        ('genre_check_name_unique',
         'UNIQUE(name)',
         'The name of the genre must be unique.')
    ]
