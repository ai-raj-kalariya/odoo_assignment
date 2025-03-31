/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";


publicWidget.registry.ContactControllerPage = publicWidget.Widget.extend({
     selector: ".fetch-btn",
     events: {
            'click': '_onFetchClick'
        },
//        ["email", "=", email ],
//        ["company_id","vat","phone","mobile","website"],
//    ])
     _onFetchClick: function(event){
        console.log("customer")
//        customer = this.pyEnv["res.partner"].search([])

     },
})