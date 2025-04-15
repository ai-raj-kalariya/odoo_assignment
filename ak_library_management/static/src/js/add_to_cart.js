/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.AddToCartWidget = publicWidget.Widget.extend({
    selector: ".add-to-cart",  // Your custom button
    events: {
        'click': '_onClickAddToCart',
    },

    _onClickAddToCart: function (event) {
        event.preventDefault();
        console.log("Add to cart button clicked");

        const $target = $(event.currentTarget);
        const productId = $target.data('product-id');  // Button should have data-product-id
        const quantity = $target.data('quantity') || 1;

        rpc('/shop/cart/add', {
            product_id: productId,
            add_qty: quantity
        }).then(function (result) {
            console.log("Product added to cart:", result);
            // Optional: show success alert, update cart counter, etc.
        });
    }
});