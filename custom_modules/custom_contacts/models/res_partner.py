# -*- coding: utf-8 -*-
from odoo import api, fields, models, modules
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = "res.partner"
    _description = 'Contact'

    commodity_id = fields.Many2many("commodity.type", string='Commodity Type')
    financial_rating = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
        ('e', 'E'),
    ], string="Financial Rating",)