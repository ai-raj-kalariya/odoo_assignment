# -*- coding: utf-8 -*-
{
    "name": "Library",
    "version": "18.0.1.1.0",
    "license": "Other proprietary",
    "depends": ["sale_management"],
    "author":"Raj",
    "website": "https://www.aktivsoftware.com",
    "data": [
        "security/ir.model.access.csv",
        "views/library_book_tags_views.xml",
        "views/library_book_category.xml",
        "views/library_library_views.xml",
        "views/library_book_views.xml",
        "views/library_member_views.xml",
        "views/product_template_views.xml",
        "views/bulk_upload_book.xml",
        "views/res_users_views.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/borrow_transaction_history_views.xml",
        "views/library_menu_views.xml",
        "data/ir_sequence_data.xml"
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}