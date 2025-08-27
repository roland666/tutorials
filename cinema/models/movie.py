from datetime import date
from logging import Logger

from odoo import fields, models, api


class Movie(models.Model):
    _name = "cinema.movie"
    _description = "Movie"

    name = fields.Char(
        required=True,
        string="Name"
    )

    description = fields.Text(
        required=False,
        string="Description"
    )

    year = fields.Integer(
        required=False,
        string="Year of release",
        default=lambda self: date.today().year
    )

    duration = fields.Integer(
        required=False,
        string="Duration (minutes)",
        default=90
    )

    # image

    genre_ids = fields.Many2many(
        comodel_name="cinema.genre",
        string="Genres"
    )

    production_company_id = fields.Many2one(
        comodel_name="cinema.production.company",
        string="Production company"
    )

    review_ids = fields.One2many(
        comodel_name="cinema.review",
        inverse_name="movie_id",
        string="Reviews"
    )

    average_rating = fields.Float(
        compute="_compute_average_rating",
        store=True
    )

    can_add_review = fields.Boolean(
        string="Can Add Review",
        compute="_compute_can_add_review"
    )

    movie_person_ids = fields.One2many(
        comodel_name="cinema.movie.person",
        inverse_name="movie_id",
        string="People"
    )

    actor_ids = fields.Many2many(
        comodel_name="cinema.person",
        compute="_compute_roles",
        string="Actors"
    )

    realisator_ids = fields.Many2many(
        comodel_name="cinema.person",
        compute="_compute_roles",
        string="Realisators"
    )

    producer_ids = fields.Many2many(
        comodel_name="cinema.person",
        compute="_compute_roles",
        string="Producers"
    )

    @api.depends("movie_person_ids")
    def _compute_roles(self):
        for movie in self:
            actors = movie.movie_person_ids.filtered(lambda mp: mp.role == "actor").mapped("person_id.id")
            realisators = movie.movie_person_ids.filtered(lambda mp: mp.role == "realisator").mapped("person_id.id")
            producers = movie.movie_person_ids.filtered(lambda mp: mp.role == "producer").mapped("person_id.id")

            movie.actor_ids = [(6, 0, actors)]
            movie.realisator_ids = [(6, 0, realisators)]
            movie.producer_ids = [(6, 0, producers)]

    @api.depends("review_ids")
    def _compute_can_add_review(self):
        self.can_add_review = True
        for movie in self:
            for review in movie.review_ids:
                if review.user_id == self.env.user:
                    self.can_add_review = False

    @api.depends("review_ids")
    def _compute_average_rating(self):
        for record in self:
            ratings = record.review_ids.mapped('rating')
            record.average_rating = sum(ratings) / len(ratings) if ratings else 0

    def action_create_review(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Review',
            'res_model': 'cinema.review',
            'view_mode': 'form',
            'view_id': self.env.ref('cinema.view_cinema_review_form').id,
            'target': 'new',
            'context': {
                'default_movie_id': self.id,
            }
        }

    def action_modify_review(self):
        self.ensure_one()
        review = self.review_ids.filtered(lambda r: r.user_id == self.env.user)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Modify Review',
            'res_model': 'cinema.review',
            'res_id': review.id,
            'view_mode': 'form',
            'view_id': self.env.ref('cinema.view_cinema_review_form').id,
            'target': 'new',
        }

    def action_delete_review(self):
        self.ensure_one()
        review = self.review_ids.filtered(lambda r: r.user_id == self.env.user)
        review.unlink()
