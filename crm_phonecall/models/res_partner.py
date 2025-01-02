# Copyright 2004-2016 Odoo SA (<http://www.odoo.com>)
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools.safe_eval import safe_eval


class ResPartner(models.Model):
    """Added the details of phonecall in the partner."""

    _inherit = "res.partner"

    phonecall_ids = fields.One2many(
        comodel_name="crm.phonecall", inverse_name="partner_id", string="Phonecalls"
    )
    phonecall_count = fields.Integer(compute="_compute_phonecall_count")

    def _compute_phonecall_count(self):
        """Calculate number of phonecalls."""
        for partner in self:
            search_domain = (
                [("partner_id.commercial_partner_id", "=", partner.id)]
                if partner.is_company
                else [("partner_id", "=", partner.id)]
            )
            partner.phonecall_count = self.env["crm.phonecall"].search_count(
                search_domain
            )

    def button_open_phonecall(self):
        self.ensure_one()
        action = self.sudo().env.ref("crm_phonecall.crm_case_categ_phone_incoming0")
        action_dict = action.read()[0] if action else {}
        action_dict["context"] = safe_eval(action_dict.get("context", "{}"))
        action_dict["context"].update(
            {
                "search_default_partner_id": self.id,
                "default_partner_id": self.id,
            }
        )
        return action_dict
