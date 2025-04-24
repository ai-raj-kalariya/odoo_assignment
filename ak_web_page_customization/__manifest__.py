# -*- coding: utf-8 -*-
{
    "name": "Custom Web Page",
    "version": "18.0.1.0.0",
    "license": "Other proprietary",
    "depends": ["hr", "website_sale",],
    "author": "Raj",
    "website": "https://www.aktivsoftware.com",
    "data": [

        "views/custom_contact_web_page_views.xml",
        "views/custom_web_menu.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'ak_web_page_customization/static/src/js/contact_web_page.js',
            'ak_web_page_customization/static/src/js/custom_web_page.js',
        ],
    },

    "installable": True,
    "auto_install": False,
    "application": False,
}
