# -*- coding: utf-8 -*-

from odoo import fields,models,api,_
from odoo.exceptions import UserError

class PricelistItemExtended(models.Model):
	_inherit = "product.pricelist.item"


	@api.model_create_multi
	def create(self, vals_list):
		res = super(PricelistItemExtended, self).create(vals_list)
		if res.pricelist_id.enable_pricelist:
			res.applied_on = '1_product'
		# else:
		# 	raise UserError("Dear User! Select pricelist is not product list view enabled")
		elif res.pricelist_id.enable_pricelist_variant:
			res.applied_on = '0_product_variant'


		return res


