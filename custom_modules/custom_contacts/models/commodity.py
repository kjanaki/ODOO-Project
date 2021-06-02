from odoo import api, fields, models, modules
from odoo.exceptions import ValidationError

class Commodity(models.Model):
	_name = "commodity.type"
	_description = "Commodity Type"
	_order = 'name'
	_inherit = 'mail.thread'

	name = fields.Char('Name',track_visibility='always',required=True)
	parent_id = fields.Many2one('commodity.type',String='Parent Commodity',track_visibility='always')

	_sql_constraints = [
	('name', 'unique (name)', 'The name already Exists!'),
	]

	def name_get(self):
		""" Return the commodity' Parent name, including their direct
			parent by default.
		"""
		res = []
		for commodity in self:
			names = []
			current = commodity
			while current:
				names.append(current.name)
				current = current.parent_id
			res.append((commodity.id, ' / '.join(reversed(names))))
		return res

		