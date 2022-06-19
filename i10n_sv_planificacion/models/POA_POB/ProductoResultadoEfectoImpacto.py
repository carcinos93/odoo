from odoo import fields, models, api


class ProductoResultadoEfectoImpacto(models.Model):
    _name = 'planificacion.producto_resultado_efecto_impacto'
    #_inherit = 'base.auditoria'

    def _codigo_generador(self):
        if self._context.get('items') is None or self._context.get('parent_codigo') is None:
            return "0"
        items = self._context.get('items')  # Todos los registros de este modelo por Resultado (modelo padre)
        parent_codigo = self.env['planificacion.resultado'].browse(self._context.get('parent_codigo'))
        filtrados = list(filter( lambda x: x[0] != 2, items))
        codigo = parent_codigo.codigo + "." + str(len(filtrados) + 1)
        return codigo

    def _periodo_default(self):
        periodo = self._context.get('periodo')
        return periodo

    producto = fields.Many2one(comodel_name='planificacion.producto', string='Producto', required=False)
    codigoProducto = fields.Char(string='Código producto', required=False, default=_codigo_generador)
    descripcionProducto = fields.Text(string="Descripción producto", required=False)
    #productoDescripcion = fields.Text(string='Producto',related='producto.descripcion', readonly=True)
    responsable = fields.Many2one('hr.employee', 'Responsable por producto')
    grupoMeta = fields.Char(string='Grupo meta', required=False)
    periodo = fields.Char(string='Periodo', size=4, default=_periodo_default)
    # vinculacion = fields.Text(string="Vinculacion", required=False)
    medioVerificacion = fields.Text(string="Medio de verificación del producto", required=False)
    indicadores = fields.One2many(comodel_name='planificacion.indicador_producto_resultado',inverse_name='productoResultado_ids',string='Indicadores',required=False, copy=True)
    actividades = fields.One2many(comodel_name='planificacion.actividad_producto_resultado',inverse_name='productoResultado_ids',string='Actividades',required=False, copy=True)
    metas = fields.One2many(comodel_name='planificacion.meta_producto_resultado',inverse_name='productoResultado_ids',string='Actividades',required=False, copy=True)

    # Modelo padre
    resultadoEfectoImpacto_ids = fields.Many2one(comodel_name='planificacion.resultado_efecto_impacto', string='Resultado efecto impacto', required=True, ondelete='cascade')
    resultadoDescripcion = fields.Text(string='Resultado',related='resultadoEfectoImpacto_ids.resultadoDescripcion', readonly=True)