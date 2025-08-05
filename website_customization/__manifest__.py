{
    "name": "Web Shop Customization",
    'version': '18.0.1.0.0',
    "license": "LGPL-3",
    "depends": ["website_sale"],
    "author": "Aktiv Software",
    "website": "https://www.aktivsoftware.com",
    "data": [
        "views/template_views.xml",
        "views/product_views.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'website_customization/static/src/js/product_data.js',
            # 'website_customization/static/src/js/product_configurator_patch.js',
        ],
    },
    "installable": True,
    "auto_install": False,
    "application": False,
}
