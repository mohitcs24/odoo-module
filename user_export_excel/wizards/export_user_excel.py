import base64
import re
from io import BytesIO
import xlsxwriter
from odoo import models, fields

class ExportUserExcel(models.TransientModel):
    _name = 'export.user.excel'
    _description = 'Export Users from JSON to Excel'

    upload_file = fields.Binary(string='Upload JSON File', required=True)

    def extract_and_export(self):
        json_data = base64.b64decode(self.upload_file).decode('utf-8')
        pattern = re.compile(
            r"_id:\s*ObjectId\('(?P<_id>[^']+)'\),\s*"
            r"firstName:\s*'(?P<firstName>[^']*)',\s*"
            r"lastName:\s*'(?P<lastName>[^']*)',\s*"
            r"email:\s*'(?P<email>[^']*)',\s*"
            r"phoneNumber:\s*'(?P<phoneNumber>[^']*)',\s*"
            r"tfn:\s*(?P<tfn>\d+),\s*"
            # r"dob:\s*ISODate\('(?P<dob>[^']+)'\)"
            r"dob:\s*ISODate\('(?P<dob>\d{4}-\d{2}-\d{2})"
        )

        matches = pattern.findall(json_data)

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Users')
        headers = ['_id', 'firstName', 'lastName', 'email', 'phoneNumber', 'tfn', 'dob']
        for col, header in enumerate(headers):
            sheet.write(0, col, header)

        for row, record in enumerate(matches, start=1):
            for col, value in enumerate(record):
                sheet.write(row, col, value)

        workbook.close()
        output.seek(0)

        attachment = self.env['ir.attachment'].create({
            'name': 'users.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'res_model': 'export.user.excel',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }
