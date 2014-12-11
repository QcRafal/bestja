# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions


class Application(models.Model):
    _inherit = 'offers.application'

    # preliminary -> first stage of recruitment
    preliminary = fields.Boolean(default=True)

    def _auto_init(self, cr, context=None):
        # Overwrite sql constraints from parent.
        # Done here as a workaround for issue #3957 in Odoo
        # https://github.com/odoo/odoo/issues/3957
        self._sql_constraints = [
            ('user_offer_uniq', 'unique("user", "offer", "preliminary")', 'User can apply for an offer only once!')
        ]
        super(Application, self)._auto_init(cr, context)

    @api.model
    def create(self, vals):
        record = super(Application, self).create(vals)
        record_sudo = record.sudo()

        # if the project is managed / coordinated by admin,
        # automatically move the application to the second
        # stage of recruitment.
        coordinator = record_sudo.offer.organization.coordinator
        manager = record_sudo.offer.project.manager
        group = 'bestja_offers_moderation.offers_moderator'
        users = self.env['res.users']

        if users.sudo(coordinator.id).has_group(group) or \
                (manager and users.sudo(manager.id).has_group(group)):
            record_sudo.preliminary = False
        return record

    @api.one
    def action_post_accepted(self):
        if self.preliminary:
            # "Move" to the second stage of recruitment
            self.sudo().create({
                'user': self.user.id,
                'offer': self.offer.id,
                'preliminary': False,
            })
        else:
            super(Application, self).action_post_accepted()

    @api.one
    def action_post_unaccepted(self):
        if self.preliminary:
            raise exceptions.ValidationError(
                "Aplikacja została przesłana do organizacji. Zmiana jej statusu nie jest już możliwa."
            )
        else:
            super(Application, self).action_post_unaccepted()