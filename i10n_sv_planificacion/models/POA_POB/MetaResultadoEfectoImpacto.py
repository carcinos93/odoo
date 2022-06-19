from odoo import fields, models, api, exceptions


class MetaResultadoEfectoImpacto(models.Model):
    _name = 'planificacion.meta_resultado_efecto_impacto'

    meta = fields.Many2one(comodel_name='planificacion.meta_resultado', string='Descripción del resultado', required=True)

    tipoValor = fields.Selection(related="meta.tipoValor")
    valor = fields.Float(related="meta.valor")

    metaTrimestre1 = fields.Char(string="I Trimestre", required=False)
    metaTrimestre2 = fields.Char(string="II Trimestre", required=False)
    metaTrimestre3 = fields.Char(string="III Trimestre", required=False)
    metaTrimestre4 = fields.Char(string="IV Trimestre", required=False)
    fechaPrevista = fields.Date(string='Fecha prevista consecución', required=False)
    # Modelo padre
    resultadoEfectoImpacto_ids = fields.Many2one(comodel_name='planificacion.resultado_efecto_impacto', string='Resultados', required=True, ondelete='cascade')

    #@api.model
    #def create(self, vals):
    #    vals['codigo'] = self._codigo_generador(vals)
    #    records = super(IndicadorActividadProductoResultado, self).create(vals)
    #    return records

    #def _codigo_generador(self, vals):
    #    parent = self.env['planificacion.producto'].search([('id', '=', str(vals['producto_ids']))])
    #    total = self.env['planificacion.indicador_producto'].search_count(
    #        [('producto_ids', '=', vals['producto_ids'])]) + 1
    #    return str(parent.codigo) + "." + str(total)