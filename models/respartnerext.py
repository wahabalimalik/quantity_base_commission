# -*- coding: utf-8 -*-

from flectra import models, fields, api

class ResPartnerExt(models.Model):
	_inherit = 'res.partner'
	
	is_contractor = fields.Boolean('Contractor')
	commission_line = fields.One2many('commission.line', 'commission_id', readonly =True)
	commission_qty_line = fields.One2many('commission.qty.line', 'commission_qty_id', readonly =True)

class CommissionLine(models.Model):
	_name = 'commission.line'

	product = fields.Many2one('product.product')
	commission = fields.Float()

	commission_id = fields.Many2one('res.partner')

class CommissionQtyLine(models.Model):
	_name = 'commission.qty.line'

	invoice = fields.Many2one('account.invoice')
	product = fields.Many2one('product.product')
	unit = fields.Float()
	qty = fields.Integer()
	total = fields.Float()
	is_paid = fields.Boolean()

	commission_qty_id = fields.Many2one('res.partner')