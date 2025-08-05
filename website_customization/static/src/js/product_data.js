/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { jsonRpc } from "@web/core/network/rpc";

publicWidget.registry.CustomCartButtonHook = publicWidget.Widget.extend({
    selector: '.oe_website_sale',

    events: {
        'click .a-submit': '_onASubmitClick',
        'click .custom-cart-add': '_onIncreaseQty',
        'click .custom-cart-sub': '_onDecreaseQty',

    },

    start: function () {
        this._super.apply(this, arguments);
        this._loadCartFromServer();
        this._bindContinueShopping();
    },

    _onASubmitClick: function (ev) {
        const $btn = $(ev.currentTarget);
        const $form = $btn.closest('form');
        const productId = parseInt($form.find('input[name="product_id"]').val(), 10);
        if (!productId)
            return;
        const $existing = $(`#custom_cart_product_${productId}`);
        setTimeout(() => {
            rpc('/custom/add_to_custom_cart', {
                product_id: productId,
            }).then((res) => {
                if (res.success) {
//                console.log('>> Add to cart clicked');
                    if ($existing.length) {
                        $existing.find('.custom-cart-qty').text(res.qty);
                        $existing.find('.custom-cart-price').text(res.price);
                    } else {
//                        console.log('>> else part Add to cart clicked');
                        this._renderProductCard(productId);
                    }
                    this._updateCartEmptyMessage();

                }
            });
       }, 300);
    },
    _updateCartEmptyMessage: function () {
        const cartItems = document.getElementById('custom_cart_items').children;
        const msg = document.getElementById('cart_empty_message');
        if (msg) {
            msg.style.display = cartItems.length > 0 ? 'none' : 'block';
            }
    },

    _onIncreaseQty: function (ev) {
    const productId = parseInt($(ev.currentTarget).data('product-id'), 10);
    this._updateCartQty(productId, 1);
    },

    _onDecreaseQty: function (ev) {
        const productId = parseInt($(ev.currentTarget).data('product-id'), 10);
        console.log("productId _onDecreaseQty......",productId)
        this._updateCartQty(productId, -1);
    },

    _updateCartQty: function (productId, deltaQty) {
        rpc('/shop/cart/update_json', {
            product_id: productId,
            add_qty: deltaQty,
            set_qty: false,
            display: true,
        }).then((res) => {
            console.log("productId......",productId)
            console.log("deltaQty......",deltaQty)
            console.log("res.cart_quantity......",res.cart_quantity)
            if res.cart_quantity >= 0 {
                // Update custom cart
                rpc('/custom/add_to_custom_cart', {
                    product_id: productId,
                    quantity_delta: deltaQty,
                }).then((result) => {
                    if (result.success) {
                        console.log("success message......")
                        const $product = $(`#custom_cart_product_${productId}`);
                        $product.find('.custom-cart-qty').text(result.qty);
                        $product.find('.custom-cart-price').text(result.price);

                        console.log("before remove product from cart......")
                        if (result.qty <= 0) {
                            console.log("remove product from cart......")
                            $product.remove();
                        }
                    this._updateCartEmptyMessage();
                    }
                });

                // Optionally update mini cart (Odoo header)
                $('.my_cart_quantity').text(res.cart_quantity);
            }
        });
    },

    _renderProductCard: function (productId, qty) {
        rpc('/custom/get_cart_products', {}).then((products) => {
            const prod = products.find(p => p.product_id === productId);
            if (prod && prod.product_html) {
                $('#custom_cart_items').append(prod.product_html);
                this._updateCartEmptyMessage();

            }
        });
    },

    _loadCartFromServer: function () {
        rpc('/custom/get_cart_products', {}).then((products) => {
        const cartContainer = document.getElementById('custom_cart_items');

        // Only proceed if container exists
        if (!cartContainer) {
            return;
        }
            products.forEach((prod) => {
                $('#custom_cart_items').append(prod.product_html);
            });
            this._updateCartEmptyMessage();
        });
    },
});