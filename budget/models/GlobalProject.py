from odoo import fields, models, api


class GlobalProject(models.Model):
    _name = 'bg.global_project'
    # _description = 'Description'

    # generales
    codigoGasto = fields.Char(string='Código gasto', required=False)
    descripcion = fields.Text(string='Descripción', required=False)
    fase = fields.Char(string='Fase', required=False)
    codigoActividad = fields.Selection(string='Código actividad',selection=[ ],required=False )
    lineaPresupuestaria = fields.Selection(string='Código de línea presupuestaria',selection=[ ],required=False )
    presupuesto = fields.Char(string='Presupuesto', required=False)
    ajuste = fields.Char(string='Ajuste', required=False)
    nuevoPresupuesto = fields.Char(string='Nuevo presupuesto', required=False)
    # pestaña ejecucion
    ejecutado1 = fields.Float(string='Ejecutado a 1 año',required=False)
    ejecutado2 = fields.Float(string='Ejecutado a 2 año',required=False)
    ejecutado3 = fields.Float(string='Ejecutado a 3 año',required=False)
    ejecutado4 = fields.Float(string='Ejecutado a 4 año',required=False)
    totalEjecutado = fields.Float(string='Total ejecutado',required=False)
    totalDisponible = fields.Float(string='Total disponible',required=False)
