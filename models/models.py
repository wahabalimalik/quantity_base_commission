# -*- coding: utf-8 -*-

from flectra import models, fields, api,_
from flectra.exceptions import UserError, ValidationError

class ProductTemplateExt(models.Model):
	_inherit = 'product.template'

	commission = fields.Float("Raising Mates PR")
	contractor = fields.Many2one('res.partner', string='Contractor' , domain=[('is_contractor', '=', True)])

	@api.multi
	def write(self, val):
		res = super(ProductTemplateExt,self).write(val)
		if self.contractor:
			rec = self.env['commission.line'].search([('product', '=', self.id)])
			if rec:
				rec.write({
					'commission' : self.commission,
		    		'commission_id' : self.contractor.id,
		    	})

			else:
				resc = self.env['commission.line'].search([('product', '=', self.id)])
				if not resc:
					rec = self.env['res.partner'].search([('id', '=', self.contractor.id)])
					rec.commission_line.create({
						'product' : self.id,
						'commission' : self.commission,
						'commission_id' : self.contractor.id,
					})

		return res

class ResPartnerExt(models.Model):
	_inherit = 'res.partner'
	
	is_contractor = fields.Boolean('Contractor')
	commission_line = fields.One2many('commission.line', 'commission_id', readonly =True)
	commission_qty_line = fields.One2many('commission.qty.line', 'commission_qty_id', readonly =True)

class AccountInvoiceExt(models.Model):
	_inherit = 'account.invoice'

	@api.multi
	def action_invoice_open(self):
		for rec in self.invoice_line_ids:
			rec.product_id.contractor.commission_qty_line.create({
				'invoice' : self.id,
				'product' : rec.product_id.product_tmpl_id.id,
				'unit' : rec.product_id.commission,
				'qty' : rec.quantity,
				'total' : rec.product_id.commission * rec.quantity,
				'commission_qty_id' : rec.product_id.contractor.id
				})

		return super(AccountInvoiceExt,self).action_invoice_open()

	@api.model
	def _cron_generate_vendor_bill(self):
		print ('sssssssssssssssssssss')
		record = self.env['res.partner'].search([
			('is_contractor','=',True),
			('supplier','=',True),
		])
		print(record)

		# for rec in record:
		# 	invoice_line_ids = []
		# 	loop = 0
		# 	for line in rec.commission_qty_line:
		# 		invoice_line_ids.append((0,loop,
		# 			{
		# 				'product_id' : line.product.id,
		# 				'name' : line.product.name,
		# 			}
		# 		))

		# 		loop = loop + 1
		# 	print(invoice_line_ids)
		# 	self.create({
		# 		'partner_id' : rec.id,
		# 		'type' : 'in_invoice',
		# 		'invoice_line_ids' : invoice_line_ids
		# 		})
		# 	print(rec.name)
		# 	print('dddddddddddddddddddddddddddddddddddddddddd')

class CommissionLine(models.Model):
	_name = 'commission.line'

	product = fields.Many2one('product.template')
	commission = fields.Float()

	commission_id = fields.Many2one('res.partner')

class CommissionQtyLine(models.Model):
	_name = 'commission.qty.line'

	invoice = fields.Many2one('account.invoice')
	product = fields.Many2one('product.template')
	unit = fields.Float()
	qty = fields.Integer()
	total = fields.Float()
	is_paid = fields.Boolean()

	commission_qty_id = fields.Many2one('res.partner')