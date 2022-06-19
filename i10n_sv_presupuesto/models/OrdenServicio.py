from odoo import fields, models, api


class OrdenServicio(models.Model):
    _name = 'presupuesto.orden_servicio'
    _description = 'Orden de servicio'
    # generales
    numeroOrden = fields.Char(string='Numero orden', required=False)
    anio = fields.Integer(string='Año', required=False)
    proveedor = fields.Char(string='Proveedor', required=False)
    fechaElaboracion = fields.Datetime(string='Fecha elaboracion')
    terminosEntrega = fields.Text(string='Numero orden', required=False)
    fuenteFinanciamiento = fields.Selection(string='Fuente de financiamiento', selection=[])
    clase = fields.Char(string='Clase', required=False)
    nombre = fields.Char(string='Nombre', required=False)
    objetivoGeneral = fields.Text(string='Objetivo general', required=False)
    plazo = fields.Char(string='Plazo', required=False)

    # obligaciones
    actividades = fields.Char(string='Actividades', required=False)
    productos = fields.Char(string='Productos', required=False)
    coordinacion = fields.Char(string='Coordinación', required=False)
    terminacion = fields.Char(string='Terminación', required=False)
    modificacion = fields.Char(string='Modificación', required=False)
    documentosIntegrantes = fields.Char(string='Documentos integrantes', required=False)
    noPagos = fields.Integer(string='No pagos', required=False)
    formaPago = fields.Char(string='Forma de pago', required=False)
    precio = fields.Float(string='Precio', required=False)
    costo = fields.Float(string='Costo', required=False)

    # firmas
    estado = fields.Char(string='Estado', required=False)
    elaboradoPor = fields.Char(string='Elaborado por', required=False)
    autorizadoPor = fields.Char(string='Autorizado por', required=False)
    aceptadoPor = fields.Char(string='Aceptado por', required=False)
