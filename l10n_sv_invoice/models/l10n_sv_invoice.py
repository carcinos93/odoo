# -*- coding: utf-8 -*-

 # -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import date, datetime


class l10nsvinvoice(models.Model):
    _name = 'sv.invoice'

    #Función que nos devuelve al usuario que está logueado
    @api.model
    def _default_user(self):
        return self._uid

    # Función que nos devuelve el dia actual
    @api.model
    def _default_date(self):
        return datetime.today()

    #Funciones que cambian el estado de una factura
    def emitir_factura(self):
        for env in self:
            env.write({'state': '2'})
        return True

    def pagar_factura(self):
        for env in self:
            env.write({'state': '3'})
        return True

    def anular_factura(self):
        for env in self:
            env.write({'state': '4'})
        return True

    #Datos de la factura
    name = fields.Char(string='Numero de factura', size=6)
    date = fields.Datetime(string='Fecha', default=_default_date)
    cashier = fields.Many2one('res.users', string='Cajero', default=_default_user)
    payment_conditions = fields.Selection([('cred', 'Crédito'),
                                           ('Cont', 'Contado'),
                                           ('otro', 'Otras condiciones')], string='Condiciones de pago')
    state = fields.Selection([
        ('1', 'Borrador'),
        ('2', 'Emitida'),
        ('3', 'Pagada'),
        ('4', 'Anulada'),
    ], default='1', string='Estado')
    observations = fields.Boolean(string='Observaciones')
    details_observations = fields.Text(string='Detalle de observaciones')


    #Datos del cliente
    client_id = fields.Many2one('sv.invoice.client', string='Cliente')
    client_nit = fields.Char(string='NIT', size=50)
    client_address = fields.Text(string='Dirección')
    client_phone = fields.Char(string='Telefono', size=12)

        #Función que nos devuelve los datos del cliente en el formulario principal

    @api.onchange('client_id')
    def ChangeClient(self):
        if self.client_id:
            self.client_nit = self.client_id.nit
            self.client_address = self.client_id.address
            self.client_phone = self.client_id.phone

    #Detalle de la factura
    invoice_details_ids = fields.One2many('sv.invoice.detail', 'details_id', string='Detalles de la factura')

    #Calculo final de la factura

    @api.depends('invoice_details_ids', 'invoice_details_ids.exempt_sales')
    def _compute_detalle(self):
        total_exempt_sales = 0.0
        for items in self.invoice_details_ids:
            total_exempt_sales += items.exempt_sales

        self.total_exempt_sales = total_exempt_sales


    total_exempt_sales = fields.Float(string='Total ventas excentas', store=True, readonly=True, compute=_compute_detalle)
    total_affected_sales = fields.Float(string='Total ventas afectas')
    total_iva = fields.Float(string='Total IVA')
    total_pay = fields.Float(string='Total a pagar')

    _order = 'state asc'

class l10nsvinvoiceclient(models.Model):
    _name = 'sv.invoice.client'

    name = fields.Char(string='Nombres', size=50)
    address = fields.Text(string='Dirección')
    nit = fields.Char(string='NIT', size=18)
    dui = fields.Char(string='DUI', size=12)
    phone = fields.Char(string='Telefono', size=12)

    is_business = fields.Boolean(string='Es empresa')
    nrc = fields.Char(string='NRC', size=12)
    sector = fields.Char(string='Sector (Industria)', size=12)
    abbreviation = fields.Char(string='Abreviatura', size=12)
    legal_representative = fields.Char(string='Nombre del representante legal', size=50)

class l10nsvinvoicedetail(models.Model):
    _name = 'sv.invoice.detail'

    name = fields.Char(string='Descripción del producto', size=50)
    quantity = fields.Float(string='Cantidad')
    amount_unit = fields.Float(string='Precio unitario')
    exempt_sales = fields.Float(string='Ventas excentas')
    affected_sales = fields.Float(string='Ventas afectas')
    taxes = fields.Selection([('iva', 'IVA'),
                                ('exec', 'Excenta')], string='Impuesto')
    iva = fields.Float(string='IVA')
    details_id = fields.Many2one('sv.invoice', string='Factura')
    sequence = fields.Integer(string='Items')

    @api.onchange('taxes')
    def ChangeAffected_sales(self):
        if self.taxes == 'iva':
            self.affected_sales = self.quantity * self.amount_unit
            self.iva = self.affected_sales * 0.13
            self.exempt_sales = 0.0

        else:
            self.affected_sales = 0.0
            self.iva = 0.0
            self.exempt_sales = self.quantity * self.amount_unit

    _defaults = {
            'sequence': 1,
        }

    _order = 'sequence asc'