/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";


publicWidget.registry.ContactControllerPage = publicWidget.Widget.extend({
     selector: ".contact-card",
     events: {
            'click': '_onContactClick'
        },
     _onContactClick: function(event){
        let contactSlug = $(event.currentTarget).data('contact-slug');
        window['location']['href'] = '/contacts/' + contactSlug;
     },
});