# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_code = fields.Char(string="Code", required=False, )

    @api.model
    def _get_custom_default_address_format(self):
        return "%(street)s\n%(street2)s\n%(city)s\n%(state_name)s\n%(country_name)s"

    def _display_custom_address(self, without_company=False):
        # get the address format
        address_format = self._get_custom_default_address_format()
        args = {
            'state_name': self.state_id.name or '',
            'country_code': self.country_id.code or '',
            'country_name': self._get_country_name(),
            'company_name': self.commercial_company_name or '',
        }
        for field in self._formatting_address_fields():
            args[field] = getattr(self, field) or ''
        if without_company:
            args['company_name'] = ''
        elif self.commercial_company_name:
            address_format = '%(company_name)s\n' + address_format
        return address_format % args

    def _get_custom_address(self, type):

        partner = self
        name = partner.name or ''
        if partner.company_name or partner.parent_id:
            if not partner.is_company:
                name = self._get_contact_name(partner, name)

        name = name + "\n" + partner._display_custom_address(without_company=True)
        if type == 'delivery' and partner.email:
            name = name + "\n" + partner.email

        if partner.phone:
            name = name + "\n" + partner.phone

        if type == 'invoice' and partner.email:
            name = name + "\n" + "Submit your invoice electronically to:" + "\n" + partner.email

        name = name.replace('\n\n', '')

        if self._context.get('html_format'):
            name = name.replace('\n', '<br/>')
        return name


