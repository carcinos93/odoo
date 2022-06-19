from odoo import fields, models, api


class FichaIndicador(models.Model):
    _name = 'planificacion.ficha_indicador'
    # _inherit = 'base.auditoria'

    @api.onchange('periodo')
    def onchange_periodo(self):
        for rec in self:
            return {'domain': {'eje': [('periodo_ids.id', '=', rec.periodo.id)]}}

    @api.onchange('eje')
    def onchange_eje(self):
        for rec in self:
            return {'domain': {'objetivoEstrategico': [('ejes_estrategicos_ids.id', '=', rec.eje.id)]}}

    @api.onchange('objetivoEstrategico')
    def onchange_objetivo(self):
        for rec in self:
            # 'meta': [('objetivo_estrategico_ids.id', '=', rec.objetivoEstrategico.id)],
            return {'domain': {'resultado': [('objetivoEstrategico_ids.id', '=', rec.objetivoEstrategico.id)]}}

    #@api.onchange('meta')
    #def onchange_meta(self):
    #    for rec in self:
    #        return {'domain': {'resultado': [('meta_ids.id', '=', rec.meta.id)]}}

    @api.onchange('resultado')
    def onchange_resultado(self):
        for rec in self:
            return {'domain': {'producto': [('resultado_ids.id', '=', rec.resultado.id)]}}

    @api.onchange('producto')
    def onchange_producto(self):
        for rec in self:
            return {'domain': {'indicador': [('producto_ids.id', '=', rec.producto.id)]}}

    # todo agregar a la vista periodo y eje
    periodo = fields.Many2one(comodel_name='planificacion.periodo', string='Seleccionar período',required=False)
    eje = fields.Many2one(comodel_name='planificacion.eje_estrategico', string='Seleccionar el eje',required=False)
    objetivoEstrategico = fields.Many2one(comodel_name='planificacion.objetivo_estrategico', string='Objetivo estratégico',required=False)
    # meta = fields.Many2one(comodel_name='planificacion.meta', string='Meta',required=False)
    resultado = fields.Many2one(comodel_name='planificacion.resultado', string='Resultado especifico al que contribuye',required=False)

    producto = fields.Many2one(comodel_name='planificacion.producto', string='Producto específico al que corresponde',required=False)
    indicador = fields.Many2one(comodel_name='planificacion.indicador_producto', string='Indicador',required=False)

    # Correspondencia
    correspondencia = fields.Text(string='Correspondencia PEI', required=False)

    # correspondencia proyecto
    correspondenciaProyectos = fields.One2many( comodel_name='planificacion.correspondencia_proyecto',inverse_name='indicador_ids', string='Correspondencia proyecto', required=False)

    # descripción
    definicionDetallada = fields.Text(string="Definición detallada", required=False)
    unidadMedida = fields.Char(string="Unidad de medida", required=False)
    desegregacion = fields.Text(string="Desegregación", required=False)
    formaCalculo = fields.Text(string="Forma de cálculo del indicador y variables", required=False)

    # correspondencia proyecto
    mediosVerificacion = fields.One2many( comodel_name='planificacion.medio_verificacion',inverse_name='indicador_ids', string='Medios de verificación', required=False)

    # recolección de datos
    frecuenciaRecolecion = fields.Char(string="Frecuencia de recolección de datos ", required=False)
    personaResponsable = fields.Char(string="Persona responsable del producto e indicador ", required=False)

    # linea base y meta
    valorLineaBase = fields.Char(string="Valor de línea base", required=False)
    metaResultado = fields.Char(string="Meta", required=False)

    # meta, todo crear grupo con nombre Meta e ingresar los 8 campos
    # meta de resultados
    metaResultadoTrim1 = fields.Char(string="I Trimestre", required=False)
    metaResultadoTrim2 = fields.Char(string="II Trimestre ", required=False)
    metaResultadoTrim3 = fields.Char(string="III Trimestre ", required=False)
    metaResultadoTrim4 = fields.Char(string="IV Trimestre ", required=False)
    # meta de productos
    metaProductoTrim1 = fields.Char(string="I Trimestre", required=False)
    metaProductoTrim2 = fields.Char(string="II Trimestre ", required=False)
    metaProductoTrim3 = fields.Char(string="III Trimestre ", required=False)
    metaProductoTrim4 = fields.Char(string="IV Trimestre ", required=False)

    # fase de analisis todo Al cambiar producto traer de planificacion.producto_resultado_efecto_impacto la vinculacion
    vinculacionProducto = fields.Text(string="Vinculación entre el producto y resultado al que contribuye ", required=False)
    fechaElaboracion = fields.Date(string='Fecha elaboración', required=False)
    fechaUltimoCambio = fields.Date(string='Fecha del último cambio', required=False)

    # cambios al indicador
    modificacionesIndicador = fields.Text(string="Modificaciones al indicador", required=False)

    # correspondencia proyecto
    desempIndicadores = fields.One2many( comodel_name='planificacion.desemp_indicador',inverse_name='indicador_ids', string='Valor de desempeño del indicador ', required=False)

    # Actividades necesarias para lograr el resultado
    actividadesResultado = fields.One2many( comodel_name='planificacion.actividad_resultado',inverse_name='indicador_ids', string='Valor de desempeño del indicador ', required=False)

    # Modelo padre
    pobpob_ids = fields.Many2one(comodel_name='planificacion.poa_pob', string='POA/POB', required=True, ondelete='cascade')
