# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    project = fields.Char()
    document_description = fields.Char()
    transport_partner_id = fields.Many2one(comodel_name="res.partner", string="Transport Company")
    truck_number = fields.Char(string="Truck Number")
    driver_name = fields.Char(string="Driver Name")
    shipper = fields.Char(string="Shipper")
    ship_date = fields.Date(string="Date", default=fields.Date.today)
    receive_date = fields.Date(string="Date")
    receiver = fields.Char(string="Receiver")
