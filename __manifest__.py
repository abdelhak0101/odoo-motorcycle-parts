# Copyright 2017-2020 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Motorcycle Parts Shop",
    "summary": "Mgc Motorcycle Parts Shop",
    "version": "17.0.1.0.0",
    "sequence": -100,
    "license": "LGPL-3",
    "website": False,
    "author": "Abdelhak",
    "category": "Warehouse Management",
    "depends": ['base', 'web', 'barcodes'],
    "data": [
        "security/ir.model.access.csv",
        "data/sequence_data.xml",
        "wizard/order_wizard_view.xml",
        "views/product_template.xml",
        "views/customer_view.xml",
        "views/order_view.xml",
        "views/menu.xml",
        "report/report.xml",
        "report/report_customer_card.xml",
        "report/report_product_card.xml",
        "report/report_orders_template.xml",

    ],
    "installable": True,
    "application": True,
}
