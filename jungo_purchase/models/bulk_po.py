from odoo import api, fields, models, modules
from odoo.exceptions import ValidationError
from datetime import datetime


class BulkPO(models.Model):
	_name = "bulk.po"
	_description = "Bulk Purchase Order"
	_inherit = 'mail.thread'


	def compute_count(self):
		for record in self:
			record.po_count = self.env['purchase.order'].search_count([('origin', '=', self.name)])

	po_count = fields.Integer('Quotations',compute='compute_count')
	name = fields.Char(string="Name",readonly=True)
	state = fields.Selection([
		('draft', 'draft'),
		('in_progress', 'In Progress'),
		('done', 'Done'),
		('cancel', 'Cancelled')
	], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True,track_visibility='always')
	create_date = fields.Date(string='Created Date', readonly=True, default=datetime.today())
	# Relational Fields
	commodity_id = fields.Many2one("commodity.type", string='Commodity Type',required=True)
	partner_ids = fields.Many2many("res.partner", string='Vendor')
	prod_ids = fields.One2many('product.line','prod_id',string='Products')
	create_uid = fields.Many2one('res.users',readonly=True,string='Created By',default=lambda self: self.env.uid)
	company_id = fields.Many2one('res.company','Company',readonly=True,index=True,default=lambda self: self.env.user.company_id.id)

	@api.model
	def create(self, vals):
		vals['name'] = self.env['ir.sequence'].next_by_code('bulk_po') or '/'
		return super(BulkPO, self).create(vals)

	def get_rfq(self):
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': 'RFQ',
			'view_mode': 'tree,form',
			'res_model': 'purchase.order',
			'domain': [('origin', '=', self.name)],
			'context': "{'create': False}"
		}

	@api.onchange('commodity_id')
	def onchange_commodity_id(self):
		if self.commodity_id:
			self.partner_ids = False
			partner_obj = self.env['res.partner'].search([('commodity_id', '=', self.commodity_id.id)])
			if partner_obj:
				self.partner_ids = partner_obj

	def action_create_rfq(self):
		purchase_obj = self.env['purchase.order']
		po_line_obj = self.env['purchase.order.line']
		if self.partner_ids:
			for data in self.partner_ids:
				create_po = purchase_obj.create({'partner_id': data.id,
												'origin': self.name,
												'company_id': self.company_id.id,
												'state': 'draft'})
				for line in self.prod_ids:
					create_line = po_line_obj.create({'product_id': line.product_id.id,
													'product_qty': line.product_qty,
													'order_id': create_po.id,
													'price_unit': line.price_unit,
													})
			self.write({'state': 'in_progress'})

class BulkPOLine(models.Model):
	_name = "product.line"
	_description = 'Product Line'


	product_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True)
	price_unit = fields.Float(string='Unit Price', digits='Product Price')
	product_id = fields.Many2one('product.product', string='Product', 
									domain=[('purchase_ok', '=', True)], change_default=True, required=True)
	prod_id = fields.Many2one('bulk.po',string='Product')


class PurchaseOrder(models.Model):
	_inherit = "purchase.order"


	def button_confirm(self):	
		res = super(PurchaseOrder, self).button_confirm()
		if self.origin:
			purchase_obj = self.env['purchase.order'].search([('origin', '=', self.origin),('id', '!=', self.id)])
			for rec in self:
				purchase_obj.write({'state': 'cancel'})
			bulk_obj = self.env['bulk.po'].search([('name', '=', self.origin),('company_id', '=', self.company_id.id)])
			if bulk_obj:
				bulk_obj.write({'state': 'done'})
		return res    