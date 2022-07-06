from odoo import fields, models, api


class AvanceIndicadorProducto(models.Model):
    _name = 'planificacion.avance_indicador_resultado'
    _description = 'Avance de indicador resultado'

    def _compute_habilitarTrimestre(self):
        # Esta variable se declara en vista monitore.xml en Evaluación del poa
        permitirEditar = self._context.get('permitir_editar', False)
        self.update({
            'habilitarTrimestre1': self._compute_configuracion('trimestre1') and permitirEditar,
            'habilitarTrimestre2': self._compute_configuracion('trimestre2') and permitirEditar,
            'habilitarTrimestre3': self._compute_configuracion('trimestre3') and permitirEditar,
            'habilitarTrimestre4': self._compute_configuracion('trimestre4') and permitirEditar
        })

    def _compute_configuracion(self, trimestre):
        configuracion = self.env['planificacion.configuracion'].search([])
        for c in configuracion:
            return getattr(c, trimestre)
        return False

    indicadorResultado = fields.Many2one(comodel_name='planificacion.indicador_resultado_efecto_impacto', string='Indicador resultado', ondelete='cascade')
    tipoValor = fields.Selection(related='indicadorResultado.unidadMedida', string='Unidad de medida')
    indicadorTrimestre1 = fields.Float(related='indicadorResultado.metaTrimestre1', string='Trimestre I')
    indicadorTrimestre2 = fields.Float(related='indicadorResultado.metaTrimestre1', string='Trimestre II')
    indicadorTrimestre3 = fields.Float(related='indicadorResultado.metaTrimestre1', string='Trimestre III')
    indicadorTrimestre4 = fields.Float(related='indicadorResultado.metaTrimestre1', string='Trimestre IV')
    puesto = fields.Many2one( comodel_name='hr.job',string='Puesto',required=False)
    trimestre1 = fields.Float(string='Trimestre I')
    trimestre2 = fields.Float(string='Trimestre II')
    trimestre3 = fields.Float(string='Trimestre III')
    trimestre4 = fields.Float(string='Trimestre IV')
    # Configuracion

    habilitarTrimestre1 = fields.Boolean(string='', compute=_compute_habilitarTrimestre)
    habilitarTrimestre2 = fields.Boolean(string='', compute=_compute_habilitarTrimestre)
    habilitarTrimestre3 = fields.Boolean(string='', compute=_compute_habilitarTrimestre)
    habilitarTrimestre4 = fields.Boolean(string='', compute=_compute_habilitarTrimestre)

    # Modelo padre
    resultadoEfectoImpacto_ids = fields.Many2one(comodel_name='planificacion.resultado_efecto_impacto', string=' Resultado específico', required=True, ondelete='cascade')
    # Consulta al modelo padre de producto resultado
    objetivoEstrategicoDetalle_ids = fields.Many2one(related='resultadoEfectoImpacto_ids.objetivoEstrategicoDetalle_ids', string='Objetivo estrátegico')
    eje_ids = fields.Many2one(related='objetivoEstrategicoDetalle_ids.eje_ids', string='Eje')
    poa_ids = fields.Many2one(related='eje_ids.poa_ids', string='POA')
