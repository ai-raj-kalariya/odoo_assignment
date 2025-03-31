/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";


publicWidget.registry.ContactControllerPage = publicWidget.Widget.extend({
     selector: ".fetch-btn",
     events: {
            'click': '_onFetchClick'
        },
//   _onFetchClick function call when button is click.
     _onFetchClick: function(event){
        var email = $('#email').val();
//      call rpc method and pass data into customer form
        rpc('/customer/fetch',{'email':email}).then(
            function(data){
            $('#name').val(data.name);
            $('#company').val(data.company);
            $('#taxID').val(data.vat);
            $('#phone').val(data.phone);
            });
     },
})