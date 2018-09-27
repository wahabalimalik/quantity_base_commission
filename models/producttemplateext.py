# -*- coding: utf-8 -*-

from flectra import models, fields, api

############################################################
# Add Two fields in Product form
# - commission :: It adds the amount of commission per product
#                 for the Contractor.That commission is created
# 				  at res.partner product tab.
# ----------------------------------------------------------
# - contractor :: It adds the contractor refferce per product
#                 That commission is created on this contractor
# 		          res.partner product tab.
#===========================================================
# Extend Write method :: Because Write mathod triger both at
# Creation and edit of page so this method watch if the product
# is in relation with respected Contractor
############################################################

class ProductTemplateExt(models.Model):
	_inherit = 'product.template'

	commission = fields.Float("Raising Mates PR")
	contractor = fields.Many2one('res.partner', string='Contractor' , domain=[('is_contractor', '=', True)])

	@api.model
	def create(self, val):
		res = super(ProductTemplateExt,self).create(val)

		product = self.env['product.product'].search([('product_tmpl_id','=',res.id)])

		resc = self.env['commission.line'].search([('product', '=', product.id)])

		if not resc:
			rec = self.env['res.partner']
			rec.commission_line.create({
				'product' : product.id,
				'commission' : res.commission,
				'commission_id' : res.contractor.id,
			})
		return res

	@api.multi
	def write(self, val):
		res = super(ProductTemplateExt,self).write(val)

		product = self.env['product.product'].search([('product_tmpl_id','=',self.id)])

		rec = self.env['commission.line'].search([('product', '=', product.id)])

		if rec:
			rec.write({
				'commission' : self.commission,
				'commission_id' : self.contractor.id,
			})

		return res