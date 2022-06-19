from odoo import fields, models, api


class Schedule(models.Model):
    _name = 'bg.schedule'
    # _description = 'Description'
    # generales
    institucionBeneficiara = fields.Char(string='Institución beneficiara', required=False)
    nombreProyecto = fields.Char(string='Nombre de proyecto', required=False)
    numeroExpediente = fields.Selection(string='Número de expediente',selection=[ ],required=False )
    periodoEjecucion = fields.Selection(string='Periodo de ejecución',selection=[ ],required=False )
    objetivo = fields.Selection(string='Objetivo',selection=[ ],required=False )
    codigoResultado = fields.Selection(string='Código de resultado',selection=[ ],required=False )
    descripcionResultado = fields.Selection(string='Descripción de resultado',selection=[ ],required=False )
    #actividades
    actividades = fields.One2many(comodel_name='bg.schedule_activities', inverse_name='scheduleActivities_ids', string='Actividades')
    montoTotal = fields.Float( string="Monto total" )


class ScheduleActivities(models.Model):
    _name = 'bg.schedule_activities'
    codigoActividad = fields.Selection(string='Código de actividad', selection=[], required=False)
    fechaInicio = fields.Datetime(string='Fecha inicio', required=False)
    fechaFin = fields.Datetime(string='Fecha fin', required=False)
    anioMes = fields.Char(string='Año/mes', required=False)
    monto = fields.Float(string='Monto', required=False)
    scheduleActivities_ids = fields.Many2one(comodel_name='bg.schedule', string='Cronograma')

