from odoo import fields, models, api


class OrdenCompra(models.Model):
    _name = 'presupuesto.orden_compra'
    _description = 'Orden de compra'

    # maestro
    numero_orden = fields.Char(string='Número orden')
    anio = fields.Integer(string='Año')
    proveedor = fields.Char(string='Proveedor')
    fecha_elaboracion = fields.Datetime(string='Fecha elaboración', required=False)
    terminos_entrega = fields.Text(string="Terminos entrega")
    observaciones = fields.Text(string="Observaciones")
    recibidoPor = fields.Char(string='Recibido por')
    elaboradoPor = fields.Char(string='Elaborado por')
    enviaGAF = fields.Char(string='Envía a GAF')
    detalle = fields.One2many(comodel_name='presupuesto.detalle_orden_compra', inverse_name='ordenCompra_ids', string='Detalle')


class OrdenCompraDetalle(models.Model):
    _name = 'presupuesto.detalle_orden_compra'
    no_correlativo = fields.Integer(string='No. Correlativo')
    descripcion = fields.Text(string="Descripción")
    cantidad = fields.Integer(string='Cantidad')
    precioUnitario = fields.Float(string='Precio unitario')
    precioTotal = fields.Float(string='Precio total')
    ordenCompra_ids = fields.Many2one(comodel_name='presupuesto.orden_compra', string='Orden compra')
