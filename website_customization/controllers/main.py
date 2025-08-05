from odoo import http
from odoo.http import request


class CustomCartController(http.Controller):

    @http.route('/custom/add_to_custom_cart', type='json', auth='public')
    def add_to_custom_cart(self, **post):
        product_id = int(post.get('product_id', 0))
        quantity_delta = int(post.get('quantity_delta', 0))

        if not product_id:
            return {'success': False}

        product = request.env['product.product'].sudo().browse(product_id)
        if not product.exists():
            return {'success': False}

        website = request.env['website'].sudo().get_current_website()
        order = website.sale_get_order()

        # Find the existing line
        order_line = order.order_line.filtered(lambda l: l.product_id.id == product_id)
        if order_line:
            new_qty = order_line.product_uom_qty

            if new_qty <= 0:
                order_line.unlink()  # Remove the line if quantity drops to 0
                qty = 0
                price = 0
            else:
                order_line.write({'product_uom_qty': new_qty})
                order_line._compute_amount()
                qty = new_qty
                price = order_line.price_subtotal
        else:
            if quantity_delta > 0:
                order._cart_update(product_id=product_id, add_qty=quantity_delta)
                order_line = order.order_line.filtered(lambda l: l.product_id.id == product_id)
                qty = order_line.product_uom_qty if order_line else 0
                price = order_line.price_subtotal if order_line else 0
            else:
                qty = 0
                price = 0

        return {
            'success': True,
            'product_id': product_id,
            'qty': qty,
            'price': price,
        }

    @http.route('/custom/get_cart_products', type='json', auth='public')
    def get_cart_products(self):
        website = request.env['website'].sudo().get_current_website()
        order = website.sale_get_order()
        result = []

        for line in order.order_line:
            product = line.product_id
            qty = line.product_uom_qty
            price = line.price_subtotal
            html = request.env['ir.ui.view']._render_template(
                'website_customization.custom_cart_product_card',
                {'product': product, 'qty': qty, 'price':price,}
            )
            result.append({
                'product_id': product.id,
                'product_html': html,
                'qty': qty,
                'price': price,
            })

        return result
