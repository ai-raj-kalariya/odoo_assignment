{
    "name": "Library",
    "version": "18.0.1.12.0",
    "license": "Other proprietary",
    "depends": ["sale_management", "hr", "stock", "base_automation","website"],
    "author": "Raj",
    "website": "https://www.aktivsoftware.com",
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",

        "report/custom_attachment_report_views.xml",
        "report/library_report_views.xml",
        "report/custom_library_report_views.xml",

        "views/library_book_tags_views.xml",
        "views/library_book_category.xml",
        "views/library_library_views.xml",
        "views/library_book_views.xml",
        "views/library_member_views.xml",
        "views/product_template_views.xml",
        "views/bulk_upload_book.xml",
        "views/res_users_views.xml",
        "views/res_partner_views.xml",
        "views/res_config_settings_viwes.xml",
        "views/sale_order_views.xml",
        "views/borrow_transaction_history_views.xml",
        "views/stock_warehouse_views.xml",
        "views/library_menu_views.xml",
        "views/custom_web_menu.xml",
        "views/custom_web_page.xml",

        "data/ir_sequence_data.xml",
        "data/ir_cron_data.xml",
        "data/ir_action_data.xml",
        "data/mail_template_data.xml",

        "wizard/borrow_warning_wizard_views.xml",
        "wizard/sale_order_wizard_views.xml",
        "wizard/borrow_transaction_history_wizard_views.xml"
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
# -*- coding: utf-8 -*-
