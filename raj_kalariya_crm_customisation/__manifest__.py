{
    "name": "CRM Customization",
    "version": "18.0.1.0.0",
    "license": "Other proprietary",
    "depends": ["sale_management", "crm", "mrp", "account", "project"],
    "author": "Raj",
    "website": "https://www.aktivsoftware.com",
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/mrp_production_views.xml",
        "views/stock_picking_views.xml",
        "views/project_project_views.xml",
        "views/account_move_views.xml",
        "views/stock_move_views.xml",
    ],

    'assets': {
        'web.assets_backend': [
            'raj_kalariya_crm_customisation/static/src/views/calendar/calendar_common/*'],
    },

    "installable": True,
    "auto_install": False,
    "application": False,
}