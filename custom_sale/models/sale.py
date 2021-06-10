from odoo import api, fields, models, modules

class SaleOrder(models.Model):
	_inherit = "sale.order"

	# @api.model
	# def sale_send_quotation(self):
	#     sale_obj = self.env['sale.order'].search([('state', '=','draft')])
	#     for sale in sale_obj:
	#         template_id = self.env.ref('sale.email_template_edi_sale')                
	#         template_id.send_mail(sale.id, force_send=True)
	#         sale.action_quotation_sent()
	#         # mail_obj.action_send_mail()

class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	@api.onchange('product_id')
	def product_id_change(self):
		res = super(SaleOrderLine, self).product_id_change()
		german_tax_id = self.env['account.tax'].search([('name','=','VAT 19%')])
		switch_tax_id = self.env['account.tax'].search([('name','=','VAT 7.7%')])
		for line in self:
			if line.order_id.partner_id.country_id.name == 'Switzerland' and line.order_id.company_id.country_id.name == 'Switzerland':
				line.tax_id = switch_tax_id
			if line.order_id.partner_id.country_id.name == 'Germany' and line.order_id.company_id.country_id.name == 'Germany':
				line.tax_id = german_tax_id
		return res