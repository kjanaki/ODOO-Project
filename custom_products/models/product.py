from odoo import api, fields, models, modules
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
	_inherit = "product.template"
	_description = "Product"


	length = fields.Char('Length')
	breadth = fields.Char('Breadth')
	height = fields.Char('Height')
	part = fields.Char('Part ID')
	revision = fields.Char('Revision')
	material = fields.Char('Material')
	lifecycle_status = fields.Char('Lifecycle Status')
	tool_no = fields.Char('Tool No')
	part_type = fields.Char('Type of Part')
	# Relational fields
	attachment_ids = fields.One2many('product.attachment','header_id',string='Attachments')

	def name_get(self):
		self.browse(self.ids).read(['name', 'default_code'])
		return [(template.id, '%s%s' % (template.default_code and '%s - ' % template.default_code or '', template.name))
				for template in self]

	class Product_Attachment(models.Model):
		_name = "product.attachment"
		_description = 'Product Attachment'

		attachment_type = fields.Selection([('specification', 'Specification'),
									        ('two_d_files', '2D Files'),
									        ('three_d_files', '3D Files'),
									        ('data_sheet', 'Data Sheet')], string="Type",)
		attachment = fields.Binary('Attachment')
		is_verified = fields.Boolean('Verified')
		verified_id = fields.Many2one('hr.employee',string='Verified By')
		header_id = fields.Many2one('product.template',string='Attachments')

class ProductProduct(models.Model):
	_inherit = "product.product"
	_description = "Product" 


	def name_get(self):
		def _name_get(d):
			name = d.get('name', '')
			code = self._context.get('display_default_code', True) and d.get('default_code', False) or False
			if code:
				name = '%s - %s' % (code,name)
			return (d['id'], name)

		partner_id = self._context.get('partner_id')
		if partner_id:
			partner_ids = [partner_id, self.env['res.partner'].browse(partner_id).commercial_partner_id.id]
		else:
			partner_ids = []
		company_id = self.env.context.get('company_id')
		self.check_access_rights("read")
		self.check_access_rule("read")

		result = []

		self.sudo().read(['name', 'default_code', 'product_tmpl_id'], load=False)

		product_template_ids = self.sudo().mapped('product_tmpl_id').ids

		if partner_ids:
			supplier_info = self.env['product.supplierinfo'].sudo().search([
				('product_tmpl_id', 'in', product_template_ids),
				('name', 'in', partner_ids),
			])

			supplier_info.sudo().read(['product_tmpl_id', 'product_id', 'product_name', 'product_code'], load=False)
			supplier_info_by_template = {}
			for r in supplier_info:
				supplier_info_by_template.setdefault(r.product_tmpl_id, []).append(r)
		for product in self.sudo():
			variant = product.product_template_attribute_value_ids._get_combination_name()

			name = variant and "%s (%s)" % (product.name, variant) or product.name
			sellers = []
			if partner_ids:
				product_supplier_info = supplier_info_by_template.get(product.product_tmpl_id, [])
				sellers = [x for x in product_supplier_info if x.product_id and x.product_id == product]
				if not sellers:
					sellers = [x for x in product_supplier_info if not x.product_id]
				if company_id:
					sellers = [x for x in sellers if x.company_id.id in [company_id, False]]
			if sellers:
				for s in sellers:
					seller_variant = s.product_name and (
						variant and "%s (%s)" % (s.product_name, variant) or s.product_name
						) or False
					mydict = {
							  'id': product.id,
							  'name': seller_variant or name,
							  'default_code': s.product_code or product.default_code,
							  }
					temp = _name_get(mydict)
					if temp not in result:
						result.append(temp)
			else:
				mydict = {
						  'id': product.id,
						  'name': name,
						  'default_code': product.default_code,
						  }
				result.append(_name_get(mydict))
		return result