from odoo import fields, models, api


class IndicadorResultadoEfectoImpacto(models.Model):
    _name = 'planificacion.indicador_resultado_efecto_impacto'
    # _inherit = 'base.auditoria'
    # todo indicador resultado debe filtrarse segun el resultado de ResultadoEfectoImpacto
    indicador = fields.Many2one(comodel_name='planificacion.indicador_resultado', string='Indicador resultado', required=True)
    nombreIndicador = fields.Char(string='Indicador nombre',related='indicador.nombre', readonly=True)
    descripcionIndicador = fields.Text(string='Indicador descripción',related='indicador.descripcion', readonly=True)
    meta = fields.Float(string='Meta',related='indicador.meta', readonly=True)
    unidadMedida = fields.Selection(string='Unidad de medida', selection=[('1', 'Porcentaje'), ('2', 'Cantidad')], required=False)
    fechaPrevista = fields.Selection(string='Fecha prevista de consecución',
                                     selection=[('1', 'I Trimestre'), ('2', 'II Trimestre'), ('3', 'III Trimestre'),
                                                ('4', 'IV Trimestre')], required=False)

    # Metas a cumplir antes de:
    metaTrimestre1 = fields.Float(string="I Trimestre", required=False)
    metaTrimestre2 = fields.Float(string="II Trimestre", required=False)
    metaTrimestre3 = fields.Float(string="III Trimestre", required=False)
    metaTrimestre4 = fields.Float(string="IV Trimestre", required=False)
    #fechaPrevista = fields.Date(string='Fecha prevista consecución', required=False)
    #Modelo padre
    resultadoEfectoImpacto_ids = fields.Many2one(comodel_name='planificacion.resultado_efecto_impacto', string='Resultado efecto impacto', required=True,ondelete='cascade')

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % (data.indicador.codigo, data.indicador.descripcion if data.indicador.descripcion else data.indicador.nombre)
            result.append((data.id, name,))
        return result

    @api.model
    def create(self, vals):
        res = super(IndicadorResultadoEfectoImpacto, self).create(vals)
        # Al crear indicador de producto se crea la linea del avance
        data = {
            'resultadoEfectoImpacto_ids': vals['resultadoEfectoImpacto_ids'],
            'indicadorResultado': res.id
        }
        self.env['planificacion.avance_indicador_resultado'].create(data)

        return res

