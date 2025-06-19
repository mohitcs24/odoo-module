import base64
from odoo import http
from odoo.http import request, content_disposition

class DocumentController(http.Controller):

    @http.route('/document/<string:access_token>', type='http', auth='public', website=True)
    def serve_file(self, access_token):
        doc = request.env['document.uploader'].sudo().search([('access_token', '=', access_token)], limit=1)
        if not doc:
            return request.not_found()

        return request.make_response(
            base64.b64decode(doc.file),  # Correct decoding of binary
            headers=[
                ('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', content_disposition(doc.filename)),
            ]
        )