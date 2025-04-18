/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";


publicWidget.registry.ProductListAddToCart = publicWidget.Widget.extend({
     selector: '.oe_website_sale',
     events: {
            'click .add_to_cart': '_onClickCart'
        },

     _onClickCart: function(ev){
        let productId = $(ev.currentTarget).data('product-id');
        rpc("/shop/cart/update_json",{'product_id': productId,'add_qty':1}).then(
            function(data){
                var $quantity = $(".my_cart_quantity")
                $quantity.text(data.cart_quantity)
            });
     }
});