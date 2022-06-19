from odoo import fields, models, api, exceptions
from datetime import  date, datetime


class i10nSvAdquisicion(models.Model):
    _name = 'prueba.adquisicion'

    @api.model
    def _default_date(self):
        return datetime.now()

    def _default_user(self):
        return self._uid

    numero_requisicion = fields.Char(string='Numero requisicion', required=True)
    empleado = fields.Many2one(comodel_name='prueba.adquisicion.empleado', string='Empleado',required=True)
    fecha_solicitud = fields.Datetime(string='Fecha de solicitud', required=False, default=_default_date)
    nombre_proyecto = fields.Char(string='Nombre proyecto', required=True)
    insumo = fields.Selection(string='Insumo', selection=[('insumo1', 'Insumo 1'), ('insumo2', 'Insumo 2'), ('insumo3', 'Insumo 3') ], required=True)
    actividad = fields.Text(string="Actividad a realizar en la cual serán utilizados los suministros o servicios", required=True)
    fecha_entrega = fields.Datetime(string='Fecha maxima de entrega de bienes o servicios',  required=False)
    lugar_entrega = fields.Char(string='Lugar de entrega', required=True)
    codigo_actividad = fields.Char(string='Codigo de actividad', required=False)
    pais_beneficiario = fields.Selection(string='Pais beneficiario',
        selection=[('01', 'Guatemala'),
                   ('02', 'Honduras'),
                   ('03', 'El Salvador'),
                   ('04', 'Nicaragua'),
                   ('05', 'Belice'),
                   ('06', 'Costa Rica'),
                   ('07', 'Panamá')],
        required=False)

    servicios = fields.One2many(
        comodel_name='prueba.adquisicion.servicios',
        inverse_name='servicios_id',
        string='Servicios',
        required=False)

    comentarios = fields.Text(string="Comentarios u observaciones")
    nombre_solicitante = fields.Char( string='Nombre solicitante', default=_default_user)

    anexos = fields.One2many(
        comodel_name='prueba.adquisicion.anexos',
        inverse_name='anexos_id',
        string='Anexos')

    @api.model
    def create(self, vals):
        template_obj = self.env['mail.template'].sudo().search([('name', '=', 'notificacion')], limit=1)

        self.action_send_amc(vals, template_obj)
        records = super(i10nSvAdquisicion, self).create(vals)
        return records

    def action_send_amc(self, vals, template_obj):
        if template_obj:
            receipt_list = ['abc@gmail.com', 'xyz@yahoo.com']
            email_cc = ['test@gmail.com']
            fecha = datetime.now().strftime('%d %b %Y')
            saludo = "Buenas tardes" if datetime.now().hour > 12 else "Buenos dias"
            body = template_obj.body_html
            body = body.replace('--saludos--', saludo )
            body = body.replace('--fecha_solicitud--', fecha)
            body = body.replace('--numero_requisicion--', vals['numero_requisicion'])

            mail_values = {
                'subject': template_obj.subject.replace('--nombre_proyecto--', vals['nombre_proyecto']),
                'body_html': body,
                'email_to': ';'.join(map(lambda x: x, receipt_list)),
                # 'email_cc': ';'.join(map(lambda x: x, email_cc)),
                'email_from': template_obj.email_from,
            }
            create_and_send_email = self.env['mail.mail'].create(mail_values).send()




class i10nAdquisicionServicios(models.Model):
    _name = 'prueba.adquisicion.servicios'
    cantidad = fields.Integer(string='Cantidad', copy=False, index=True)
    descripcion = fields.Text(string="Descripcion",required=True)
    monto_presupuestado = fields.Float(string='Monto presupuestado', required=True)
    linea_presupuestaria = fields.Selection(string='Linea presupuestaria', selection=[('1', 'F.6.1'), ('2', 'F.7.2'), ], required=False )
    categoria_gasto = fields.Selection(string='Categoría del gasto', selection=[('1', 'Consulting to assets') ],required=False )
    linea_presupuestaria_poa = fields.Selection(
        string='Linea presupuestaria POA',
        selection=[('1', '2.3.2.4') ],
        required=False, )
    servicios_id = fields.Many2one(
        comodel_name='prueba.adquisicion',
        string='Aquisicion')

    @api.model
    def create(self, vals):
        vals['cantidad'] = self.env['ir.sequence'].next_by_code('adquisicion_servicios_cantidad')
        records = super(i10nAdquisicionServicios, self).create(vals)
        return records


class i10nSvAdquisicionEmpleado(models.Model):
    _name = 'prueba.adquisicion.empleado'

    nombre = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=False)

class i18SvAdquisicionAnexos(models.Model):
    _name = 'prueba.adquisicion.anexos'

    anexo = fields.Binary(string="Anexo" )
    anexo_nombre = fields.Char(string="Anexo nombre")
    anexos_id = fields.Many2one(comodel_name='prueba.adquisicion', string='Aquisicion')

