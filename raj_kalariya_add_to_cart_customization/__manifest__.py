# -*- coding: utf-8 -*-
{
    "name": "Add to cart",
    "version": "18.0.1.0.0",
    "license": "Other proprietary",
    "depends": ["stock", "website_sale"],
    "author": "Raj",
    "website": "https://www.aktivsoftware.com",
    "data": [
        "security/ir.model.access.csv",
        "views/templates_inherit_views.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'raj_kalariya_add_to_cart_customization/static/src/js/add_to_cart.js',
        ],
    },

    "installable": True,
    "auto_install": False,
    "application": False,
}
