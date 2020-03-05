import logging
from datetime import datetime
from odoo import fields, models, exceptions, _, api
from datetime import timedelta
import pytz
from pytz import timezone
from odoo.exceptions import ValidationError
import base64
import codecs
import io
from io import BytesIO

_logger = logging.getLogger(__name__)


class TransfersReportXlsx(models.AbstractModel):
    _name = 'report.edc_stock_reports.transfers_report_xlsx'
    _inherit = 'report.odoo_report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        user_tz = timezone(self.env.user.tz or 'UTC')
        sheet = workbook.add_worksheet('sheet')
        stock_obj = self.env['stock.picking']

        logo = self.env.user.company_id.logo
        image_data = BytesIO(base64.b64decode(logo))
        header_format = workbook.add_format({
            'bold': 1,
            'border': 2,
            'align': 'center',
            'valign': 'vcenter',
            'color': 'black',
            'font_size': 16,

        })
        header_format2 = workbook.add_format({
            'border': 2,
            'align': 'center',
            'valign': 'vcenter',
            'color': 'black',

        })
        left_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 2,
            'bg_color': '#51AFF4',

        })
        left_format2 = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 2,
            'bg_color': '#51AFF4',
            'font_size': 14,

        })
        center_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 2,
            'color': 'black',

        })
        sr_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 2,
            'color': 'black',
            'bg_color': '#7EC3F5',

        })
        sheet.set_column('A:H', 20)
        sheet.set_row(0, 25)
        sheet.set_row(1, 25)
        sheet.set_row(2, 25)
        # Header of Report data ,titles
        sheet.insert_image("A1:B3", 'logo.png', {'image_data': image_data, 'x_scale': 0.49, 'y_scale': .35})
        sheet.merge_range("B1:E3", _("GARGO MANIFEST (CM)"), header_format)
        sheet.write("F1", _("Doc NO:"), header_format2)
        sheet.write("F2", _("Revision NO:"), header_format2)
        sheet.write("F3", _("Rev Date:"), header_format2)
        sheet.write("A5", _("CM NO:"), left_format)
        sheet.write("A6", _("Date:"), left_format)
        sheet.write("A8", _("From:"), left_format)
        sheet.write("D8", _("TO:"), left_format)

        sheet.write("G1", '', header_format2)
        sheet.write("G2", '', header_format2)
        sheet.write("G3", '', header_format2)
        sheet.write("B5", objects.name, header_format2)
        sheet.write("B6", str(objects.scheduled_date), header_format2)
        sheet.write("B8", objects.location_id.display_name, header_format2)
        sheet.write("E8", objects.location_dest_id.display_name, header_format2)

        sheet.merge_range("A9:A10", _("Item"), left_format)
        sheet.merge_range("B9:B10", _("Description"), left_format)
        sheet.merge_range("C9:C10", _("Part NO./asset#"), left_format)
        sheet.merge_range("D9:D10", _("Qty"), left_format)
        sheet.merge_range("E9:E10", _("Unit"), left_format)
        sheet.merge_range("F9:F10", _("Remarks"), left_format)
        sheet.merge_range("G9:H9", _("Reimbursable"), left_format)
        sheet.write("G10", _("YES"), left_format)
        sheet.write("H10", _("NO"), left_format)

        row = 10
        col = 0
        count = 1
        for line in objects.move_ids_without_package:
            sheet.write(row, col, count, sr_format)
            sheet.write(row, col + 1, line.description_picking or '', center_format)
            sheet.write(row, col + 2, line.product_id.barcode or '', center_format)
            sheet.write(row, col + 3, line.product_uom_qty or '', center_format)
            sheet.write(row, col + 4, line.product_uom.name or '', center_format)
            sheet.write(row, col + 5, line.remarks or '', center_format)
            sheet.write(row, col + 7, "X" or '', center_format)
            sheet.write(row, col + 6, '', center_format)
            row += 1
            count += 1

        sheet.write(row + 3, col, _("Shipper"), left_format)
        sheet.write(row + 4, col, _("Date&Signature"), left_format)
        sheet.write(row + 7, col, _("Receiver"), left_format)
        sheet.write(row + 8, col, _("Date&Signature"), left_format)
        sheet.merge_range(row + 3, col + 5, row + 3, col + 6, _("Transportation Details"), left_format2)
        sheet.write(row + 4, col + 5, _("Transport Company"), left_format)
        sheet.write(row + 5, col + 5, _("Truck Number"), left_format)
        sheet.write(row + 6, col + 5, _("Driver Name"), left_format)
        sheet.write(row + 7, col + 5, _("Signature"), left_format)

        sheet.write(row + 3, col + 1, objects.shipper, header_format2)
        sheet.write(row + 4, col + 1, str(objects.ship_date), header_format2)
        sheet.write(row + 7, col + 1, objects.receiver, header_format2)
        sheet.write(row + 8, col + 1, str(objects.receive_date), header_format2)
        sheet.write(row + 4, col + 6, objects.transport_partner_id.display_name, header_format2)
        sheet.write(row + 5, col + 6, objects.truck_number, header_format2)
        sheet.write(row + 6, col + 6, objects.driver_name, header_format2)
        sheet.write(row + 7, col + 6, '', header_format2)
