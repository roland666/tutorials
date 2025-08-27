from odoo import fields, models


class Person(models.Model):
    _name = "cinema.person"
    _description = "Can be an actor, producer, realisator"

    name = fields.Char(string="Person", required=True)
    birthdate = fields.Date(string="Date of birth")
    biography = fields.Char(string="Biography")

    # image
