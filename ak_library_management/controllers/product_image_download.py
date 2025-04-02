# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, content_disposition
import base64
import io
import zipfile


class ProductImageDownload(http.Controller):
    """
    Odoo Controller to download product images.
    This class provides an HTTP route that allows users to download product images.
    If a single image is found, it is returned directly. If multiple images exist,
    they are packaged into a ZIP file.
    """
    @http.route([
        # '/download_images',
        '/download_images/<model("product.template"):product>',
    ], type='http', auth='public')
    def download_product_image(self, product=None):
        """
        Fetches all product images and provides them as downloadable files.
          - If there is only one image, it will be downloaded directly.
          - If multiple images exist, a ZIP file containing all images is created and returned.
        Returns:
            HTTP Response: Single image file or a ZIP archive.
        """
        product_image_id = request.env['product.image'].sudo().search([
            ("product_tmpl_id", "=", product.id)
        ])
        if len(product_image_id) == 1:
            image_data = base64.b64decode(product_image_id.image_1920)
            return request.make_response(image_data, [
                ('Content-Type', ''),
                ('Content-Disposition', content_disposition(f"{product_image_id.name}"))
            ])

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for img in product_image_id:
                image_data = base64.b64decode(img.image_1920)
                zip_file.writestr(img.name, image_data)
        zip_buffer.seek(0)
        return request.make_response(zip_buffer.getvalue(), [
            ('Content-Type', 'application/zip'),
            ('Content-Disposition', content_disposition('images.zip'))
        ])
