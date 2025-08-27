from odoo import models, fields, api
from odoo.exceptions import AccessError, ValidationError


class Review(models.Model):
    _name = "cinema.review"
    _description = "Movie Review"

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        required=True,
        default=lambda self: self.env.user,
        readonly=True
    )

    movie_id = fields.Many2one(
        comodel_name="cinema.movie",
        string="Movie",
        required=True
    )

    rating = fields.Integer(
        string="Rating (0-10)",
        required=True
    )

    comment = fields.Text(
        string="Comment"
    )

    _sql_constraints = [
        ('unique_user_movie', 'unique(user_id, movie_id)',
         'You can only review a movie once!')
    ]

    @api.constrains('rating')
    def _check_rating(self):
        for rec in self:
            if rec.rating < 0 or rec.rating > 10:
                raise ValidationError("Rating must be between 0 and 10!")

    def write(self, vals):
        if self.user_id != self.env.user:
            raise AccessError("You can only edit your own reviews!")
        return super().write(vals)

    def unlink(self):
        if any(r.user_id != self.env.user for r in self):
            raise AccessError("You can only delete your own reviews!")
        return super().unlink()
