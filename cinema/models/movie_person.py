from odoo import fields, models


class MoviePerson(models.Model):
    _name = "cinema.movie.person"
    _description = "Relation table between person, role and movie"

    movie_id = fields.Many2one(comodel_name="cinema.movie", required=True)
    person_id = fields.Many2one(comodel_name="cinema.person", required=True)
    role = fields.Selection([
        ("actor", "Actor"),
        ("realisator", "Pealisator"),
        ("producer", "Producer")
    ], string="Role", required=True)
