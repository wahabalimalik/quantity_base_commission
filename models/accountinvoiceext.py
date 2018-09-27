# -*- coding: utf-8 -*-

from flectra import models, fields, api

# ##################################################
# Performing two major oprations
# 1- On the time of validating invoice calculate the 
#    commission of contractor.By extending funtion
#    action_invoice_open()
# 2- A cronical action perform for auto genration of 
#   vendor bill for Contractors br creating 
#  _cron_generate_vendor_bill() function
# ###################################################3

class AccountInvoiceExt(models.Model):
	_inherit = 'account.invoice'

	@api.multi
	def action_invoice_open(self):
		print('ddddddddddddddddddd')
		for rec in self.invoice_line_ids:
			rec.product_id.contractor.commission_qty_line.create({
				'invoice' : self.id,
				'product' : rec.product_id.id,
				'unit' : rec.product_id.commission,
				'qty' : rec.quantity,
				'total' : rec.product_id.commission * rec.quantity,
				'commission_qty_id' : rec.product_id.contractor.id
				})

		return super(AccountInvoiceExt,self).action_invoice_open()

	@api.model
	def _cron_generate_vendor_bill(self):
		record = self.env['res.partner'].search([
			('is_contractor','=',True),
			('supplier','=',True),
		])

		for rec in record:
			invoice_line_ids = []
			loop = 0
			for line in rec.commission_qty_line:
				if not line.is_paid:
					invoice_line_ids.append((0,loop,
						{
							'product_id' : line.product.id,
							'name' : line.product.name,
							'account_id' : 19,
							'quantity' : line.qty,
							'price_unit' :line.unit,
						}
					))

				line.is_paid = True

				loop = loop + 1

			if invoice_line_ids:

				invoice_id = self.create({
					'partner_id' : rec.id,
					'type' : 'in_invoice',
					'invoice_line_ids' : invoice_line_ids,

				})