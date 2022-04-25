# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Requisition Order Type",
    "version": "14.0.1.0.2",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Purchase Management",
    "depends": ["bi_material_purchase_requisitions"],
    "website": "https://github.com/OCA/purchase-workflow",
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/view_requisition_order_type.xml",
        "views/view_requisition_order.xml",
        "data/requisition_order_type",
    ],
    "installable": True,
    "auto_install": False,
}
