from odoo import models, fields, api
import uuid

class UploadedDocument(models.Model):
    _name = 'document.uploader'
    _description = 'Uploaded Documents'

    name = fields.Char(string="File Name")
    file = fields.Binary(string="File", required=True)
    filename = fields.Char(string="Filename")
    access_token = fields.Char(string="Access Token", readonly=True)
    url = fields.Char(string="Public URL", compute="_compute_url", store=True)

    @api.model
    def create(self, vals):
        vals['access_token'] = str(uuid.uuid4())
        return super().create(vals)

    @api.depends('access_token')
    def _compute_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            record.url = f"{base_url}/document/{record.access_token}"
