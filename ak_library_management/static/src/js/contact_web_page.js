/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";


publicWidget.registry.ContactControllerPage = publicWidget.Widget.extend({
     selector: ".partner-card",
     events: {
            'click': '_onContactClick'
        },
     _onContactClick: function(ev){
        let contactSlug = $(ev.currentTarget).data('contact-slug');
        window['location']['href'] = '/contacts/' + contactSlug;
     },
});