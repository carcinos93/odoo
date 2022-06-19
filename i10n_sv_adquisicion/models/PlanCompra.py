from odoo import fields, models, api


class PlanCompra(models.Model):
    _name = 'adquisicion.plan_compra'
    _description = 'Plan de compras'

    fuente_financimiento = fields.Selection(string='Fuente financimiento', selection=[])
    actividad_proyecto = fields.Char(string='Actividad proyecto')
    categoria_gasto = fields.Selection(string='Categoría del gasto', selection=[])
    cod_act_poa = fields.Selection(string='Cod. act. de POA ', selection=[])
    actividad = fields.Char(string='Actividad')
    procesos_compra = fields.Char(string='Procesos de compra')
    insumo = fields.Char(string='Insumo')
    costo_financiado = fields.Float(string='Costo total financiado')
    costo_nofinanciado = fields.Float(string='Costo total no financiado')
    presupuesto_ajustado = fields.Float(string='Presupuesto ajustado')
    total_presupuesto_ajustado = fields.Float(string='Total, de presupuesto ajustado')
    ejecucion = fields.Float(string='Ejecución')
    ejecucion_trimestre = fields.Float(string='Ejecución por trimestre')
    total_ejecucion = fields.Float(string='Total de ejecución')
    disponibilidad = fields.Float(string='Disponibilidad')
    disponibilidad_trimestre = fields.Float(string='Disponibilidad por trimestre')
    total_disponibilidad = fields.Float(string='Disponibilidad por trimestre')
    pais = fields.Selection(string='País', selection=[])
    observaciones = fields.Text(string="Observaciones")






        
