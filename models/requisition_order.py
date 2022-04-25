# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase


class MaterialPurchaseRequisition(models.Model):
    _inherit = "material.purchase.requisition"

    order_type = fields.Many2one(
        comodel_name="requisition.order.type",
        readonly=False,
        states=Purchase.READONLY_STATES,
        string="Type",
        ondelete="restrict",
        domain="[('company_id', 'in', [False, company_id])]",
    )

    @api.onchange("order_type")
    def onchange_order_type(self):
        for order in self:
            if order.order_type.payment_term_id:
                order.payment_term_id = order.order_type.payment_term_id.id
            if order.order_type.incoterm_id:
                order.incoterm_id = order.order_type.incoterm_id.id

    @api.model
    def create(self, vals):
        if vals.get("sequence", "/") == "/" and vals.get("order_type"):
            requisition_type = self.env["requisition.order.type"].browse(vals["order_type"])
            if requisition_type.sequence_id:
                vals["sequence"] = requisition_type.sequence_id.next_by_id()
        return super().create(vals)

    @api.constrains("company_id")
    def _check_po_type_company(self):
        if self.filtered(
            lambda r: r.order_type.company_id
            and r.company_id
            and r.order_type.company_id != r.company_id
        ):
            raise ValidationError(_("Document's company and type's company mismatch"))

    def _default_order_type(self):
        return self.env["requisition.order.type"].search(
            [("company_id", "in", [False, self.company_id.id])],
            limit=1,
        )

    @api.onchange("company_id")
    def _onchange_company(self):
        self.order_type = self._default_order_type()
