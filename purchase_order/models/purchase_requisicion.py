 # -*- coding: utf-8 -*-
from odoo import models, fields, api , _, tools, exceptions
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError
import webbrowser

class purchase_order(models.Model):
    _inherit = 'purchase.order'

    requisicion_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')

class purchaseSequences(models.Model):
    _name = 'purchase.sequences'

    program_id = fields.Many2one('budget.program', 'Proyecto')
    correlative_id = fields.Char('Correlativo')

    def next_correlativo(self):
        self.correlative_id = str(int(self.correlative_id) + 1)

purchaseSequences()

class purchaseRequisicion(models.Model):
    _name = 'purchase.order.requisitions'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    # Función que nos devuelve al usuario que está logueado
    @api.model
    def _default_user(self):
        return self._uid

    @api.depends('program_id', 'state')
    def _compute_name(self):
        if self.program_id:
            if self.state == '0':
                self.name = 'Requisición borrador'
                self.name_corto_program = self.program_id.shortName
            else:
                corre_this = self.env['purchase.sequences'].search([('program_id', '=', self.program_id.id)])
                correlativo = 'NE'
                if corre_this:
                    correlativo = corre_this.correlative_id
                axo = date.today().year
                self.name = self.program_id.shortName + '/' + correlativo + '/' + str(axo)
                self.name_corto_program = self.program_id.shortName

    name = fields.Char('Correlativo', compute='_compute_name', store=True, readonly=True)
    program_id = fields.Many2one('budget.program', 'Proyecto')
    name_corto_program = fields.Char('Proyecto')
    solicitante = fields.Many2one('hr.employee', 'Autorizador')
    type = fields.Many2one('purchase.type', 'Tipo de Compra')
    activity_id = fields.Many2one('planificacion.actividad_producto_resultado', 'Actividad')
    date_order = fields.Date('Fecha de Entrega', help='Fecha Maxima de Entrega')
    place_delivery = fields.Text('Lugar de Entrega')
    activity = fields.Char('Actividad Nombre')
    country_id = fields.Many2many(
        'res.country', string='Paises beneficiarios',
    )
    state = fields.Selection([('1', 'Requisicion'),
                              ('2', 'Selección'),
                              ('3', 'Formalización'),
                              ('4', 'Recepcion'),
                              ('5', 'Pago')], default='1', string='Estado',  tracking=True)


    doc_formalizar = fields.Selection([('1', 'Orden de Compra'),
                              ('2', 'Orden de Servicio'),
                              ('3', 'Contrato')], 'Documento para Formalizar', tracking=True)
    applicant = fields.Char('Autorizador')
    evento = fields.Char(string='Actividad / Evento')
    comment = fields.Text(string='Comentarios')
    date_applicant = fields.Datetime('Fecha Solicitante')
    authorizer = fields.Char('Autorizador')
    date_authorizer = fields.Datetime('Fecha de Autorizacion')
    purchase_author = fields.Char('Autoriza Compras')
    date_purchase_author = fields.Datetime('Fecha Compras Autoriza')
    purchase_docs_ids = fields.One2many('purchase.order.docs', 'requisition_id', 'doc')
    purchase_requi_line_ids = fields.One2many('purchase.order.requisition.line', 'requisition_id', 'Lineas')
    authorizer_ids = fields.One2many('purchase.order.autorizacion', 'requisition_id', 'Autorizacion')
    lineas_order_ids = fields.One2many('purchase.line.requisicion', 'requisition_id', 'Lineas de Orden de Compra')
    lineas_oferta_ids = fields.One2many('purchase.order.ofertas', 'requisition_id', 'Lineas de Ofertas')
    lineas_adjudicacion = fields.One2many('purchase.order.adjudicacion', 'requisition_id', 'Lineas Adjudicacion')
    lineas_proveedores = fields.Many2many('res.partner', 'reequisicion_partner_rel', 'rquisicion_id', 'partner_ids', 'Proveedores')
    orden_compra_ids = fields.One2many('purchase.order', 'requisicion_id', 'Ordenes de Compra')
    orden_servicio_ids = fields.One2many('purchase.order.service', 'requisicion_id', 'Ordenes de Servicio')
    used_comite = fields.Boolean(string='Utiliza Cómite Evaluador')
    date_requisicion = fields.Date(string='Fecha Requisición')
    evaluacion_ids = fields.One2many('purchase.order.evaluacion', 'order_id', string='Evalaución')
    adjudicacion_ids = fields.One2many('purchase.line.requisicion.adjudicacion', 'adjudicacion_ids', string='adjudicacion_ids')

    evaluaciones_ids = fields.One2many('purchase.order.comite.evaluacion', 'order_id', string='Evaluaciones')


    comite_ids = fields.Many2many('hr.employee', 'comite_requision_employee_rel', 'order_id', 'employee_id', string='Comité')
    filename_comite = fields.Char(string='Nombre Archivo')
    file_comite = fields.Binary('Nombramiento Comité')
    filename_comite_form = fields.Char(string='Nombre Archivo')
    file_comite_form = fields.Binary('Formulario de Comité')
    proceso_iniciado = fields.Boolean(string='Proceso Iniciado', tracking=True)
    proceso_autorizado = fields.Boolean(string='Proceso Autorizado', tracking=True)

    nombre_solicitante = fields.Many2one('res.users', string='Solicitante', default=_default_user)
    gestor = fields.Many2one('hr.employee', 'Gestor')
    contrato_ids = fields.One2many('purchase.order.requisitions.contrato', 'contrato_ids',
                                                string='Contrato')
    # Calculo final del total de la requisicion

    @api.depends('purchase_requi_line_ids', 'purchase_requi_line_ids.monto')
    def _compute_detalle(self):
        monto_requisicion = 0.0
        for items in self.purchase_requi_line_ids:
            monto_requisicion += items.monto

        self.monto_requisicion = monto_requisicion

    monto_requisicion = fields.Float(string='Monto Requisición ', store=True, readonly=True,
                                      compute=_compute_detalle)

    def actionPrint(self):
       return {
           'type': 'ir.actions.act_url',
           'url': 'http://72.167.53.164:8080/birt/frameset?__report=compras_requisicion.rptdesign&id='+str(self.id)
       }



    @api.onchange('program_id')
    def onchange_program(self):
        #corre_this = self.env['purchase.sequences'].search([('program_id', '=', self.program_id.id)])
        if self.program_id:
            self.name = self.program_id.shortName

    @api.onchange('type')
    def onchange_type(self):
        self.used_comite = self.type.used_comite

    @api.onchange('activity_id')
    def onchange_activity(self):
        self.activity = self.activity_id.nombreActividad

    def RetornarEtapa(self):
        estado = '1'
        obj_val = self.env['purchase.order.autorizacion']
        if self.state == '2':
            estado = '1'
            vals = {'name': 'Regresa a etapa de Requisición',
                    'type': 'auto',
                    'user_id': self.env.uid,
                    'date_acc': datetime.today(),
                    'requisition_id': self.id}
            obj_val.create(vals)
        if self.state == '3':
            estado = '2'
            vals = {'name': 'Regresa a etapa de Selección',
                    'type': 'auto',
                    'user_id': self.env.uid,
                    'date_acc': datetime.today(),
                    'requisition_id': self.id}
            obj_val.create(vals)
        if self.state == '4':
            estado = '3'
            vals = {'name': 'Regresa a etapa de Formalización',
                    'type': 'auto',
                    'user_id': self.env.uid,
                    'date_acc': datetime.today(),
                    'requisition_id': self.id}
            obj_val.create(vals)
        if self.state == '5':
            estado = '4'
            vals = {'name': 'Regresa a etapa de Recepción',
                    'type': 'auto',
                    'user_id': self.env.uid,
                    'date_acc': datetime.today(),
                    'requisition_id': self.id}
            obj_val.create(vals)
        self.write({'state': estado})

    def IniciarProceso(self):
        if self.monto_requisicion == 0.0:
            raise ValidationError(
                _('Lo siento no puede iniciar el proceso, el monto de requisición es 0.0.'))
        corre_this = self.env['purchase.sequences'].search([('program_id', '=', self.program_id.id)])
        corre_this.next_correlativo()
        self.write({'proceso_iniciado': True})
        vals = {'name': 'Inicio del Proceso',
                'type': 'auto',
                'user_id': self.env.uid,
                'date_acc': datetime.today(),
                'requisition_id': self.id}

        obj_val = self.env['purchase.order.autorizacion']
        obj_val.create(vals)
        return True

    def AutorizarRequisicion(self):
        if not self.proceso_iniciado:
            raise ValidationError(
                _('El proceso no se puede autorizar, sino se ha iniciado. Comuniquese con el Solicitante'))

        self.write({'proceso_autorizado': True})
        vals = {'name': 'Autoriza Requisición',
                'type': 'auto',
                'user_id': self.env.uid,
                'date_acc': datetime.today(),
                'requisition_id': self.id}

        obj_val = self.env['purchase.order.autorizacion']
        obj_val.create(vals)
        return True

    def RetrocederInicio(self):
        res = dict()
        if self.proceso_iniciado:
            res['proceso_iniciado'] = False
            vals = {'name': 'Regresa a inicio',
                    'type': 'auto',
                    'user_id': self.env.uid,
                    'date_acc': datetime.today(),
                    'requisition_id': self.id}
            obj_val = self.env['purchase.order.autorizacion']
            obj_val.create(vals)

        if self.proceso_autorizado:
            res['proceso_autorizado'] = False
            vals = {'name': 'Regresa a inicio',
                    'type': 'auto',
                    'user_id': self.env.uid,
                    'date_acc': datetime.today(),
                    'requisition_id': self.id}
            obj_val = self.env['purchase.order.autorizacion']
            obj_val.create(vals)

        self.write(res)
        return True

    def autorizacion_partner(self):
        if not self.proceso_autorizado:
            raise ValidationError(
                _('No se puede aceptar la compra, si su debida autorización. Comuniquese con el encargado de autorizar.'))

        today = date.today()
        if self.date_order < today:
            raise ValidationError(
                _('La fecha de entrega, no puede ser menor a la fecha actual.'))

        documentos1 =''
        for documentos in self.purchase_docs_ids:
            if documentos.name.mandatory is True:
                documentos1 += ' ' + documentos.name.name
        ducumentos2 = ''

        libres = self.env['purchase.type.doc'].search([('type_id', '=', self.type.id), ('state_author', '=', self.state)])
        for documentos in libres:
            if documentos.mandatory is True:
                ducumentos2 += ' ' + documentos.name
        if documentos1 == ducumentos2:
            raise exceptions.ValidationError('Debe seleccionar los documentos del proyecto')


        vals2 = {'name': 'Aceptación de Compra',
                'type': 'auto',
                'user_id': self.env.uid,
                'date_acc': datetime.today(),
                'requisition_id': self.id}
        obj_val = self.env['purchase.order.autorizacion']
        obj_val.create(vals2)
        self.write({
                    'state': '2',
                    'date_requisicion': date.today()
                    })
        #### Actualizando los valores de la actividad
        for item in self.purchase_requi_line_ids:
            if item.insumo_id:
                reservado = item.insumo_id.reservado + item.monto
                item.insumo_id.write({'reservado': reservado})

        return True

    def pasoFormalizacion(self):
        today = date.today()

        if self.date_order < today:
            raise ValidationError(
                _('La fecha de entrega, no puede ser menor a la fecha actual.'))


        user_browse = self.env['res.users'].browse(self.env.uid)
        vals = {'name': 'Paso a Formalización',
                'type': 'auto',
                'user_id': self.env.uid,
                'date_acc': datetime.today(),
                'requisition_id': self.id}

        obj_val = self.env['purchase.order.autorizacion']
        obj_val.create(vals)
        self.write({'state': '3'})



    def adjudicar(self):
            for item in self.lineas_order_ids:
                res = {
                        'name': item.proveedor.id,
                        'monto_ad': item.price_unitary_ad,
                        'adjudicacion_ids': item.requisition_id.id,
                        'date_order': datetime.today(),
                        }

                orden_id = self.env['purchase.line.requisicion.adjudicacion'].create(res)
            return True

    @api.constrains('lineas_order_ids')
    def _exist_record_in_line(self):
        for record in self:
            exist_record_lines = []
            for line in record.lineas_order_ids:
                if line.name.id in exist_record_lines:
                    raise ValidationError('No puede agregar un proveedor que ya ha sido seleccionado')
                exist_record_lines.append(line.name.id)



        #order = adj_obj.create(crea_order)

                #for items in detAd.lineas_order_ids:
                    #crea_lineas = {
                    #    'det_adjudicacion_ids': order.id,
                    #    'name': items.name,
                    #    'monto_linea': items.monto_ad,
                    #}
                    #             adj_line_obj.create(crea_lineas)




        #for detAd in self.lineas_order_ids:

           #if not detAd.lineas_order_ids:
               #det = det_obj.search([('name', '=', detAd.proveedor.id)])
               #if not det:
                   # res_l = {
                      #  'name': detAd.proveedor.id,
                      #  'monto_ad': 0,
                      #  'adjudicacion_ids': detAd.requisition_id.id,
                       # 'date_order': datetime.today(),
                   # }
                  #  adj_obj.create(res_l)





    def ordenes_compras(self):
        orden_compra = self.env['purchase.order']
        orden_compra_lineas = self.env['purchase.order.line']
        if self.lineas_adjudicacion:
            for adj in self.lineas_adjudicacion:
                if adj.adjudication == True:
                    crea_order = {
                        'requisicion_id': self.id,
                        'partner_id': adj.name.id,
                        'date_order': datetime.today(),
                        'currency_id': adj.name.property_purchase_currency_id.id or 2,
                        'state': 'purchase',
                        'user_id': self.env.uid
                    }
                    order = orden_compra.create(crea_order)
                    for items in adj.lineas_adjudicacion:
                        crea_lineas = {
                            'order_id': order.id,
                            'name': items.name,
                            'product_id': items.product_id.id,
                            'product_qty': items.cantidad,
                            'product_uom_qty': items.cantidad,
                            'price_unit': items.price_unitary,
                            'price_subtotal': items.monto,
                            'price_total': items.monto,
                            'company_id': 1,
                            'state': 'purchase'
                        }
                        orden_compra_lineas.create(crea_lineas)

        vals = {'name': 'Cierre del Proceso',
                'type': 'auto',
                'user_id': self.env.uid,
                'date_acc': datetime.today(),
                'requisition_id': self.id}

        obj_val = self.env['purchase.order.autorizacion']
        obj_val.create(vals)
        self.write({'state': '4'})

        #### Actualizando los valores de la actividad
        for item in self.purchase_requi_line_ids:
            if item.insumo_id:
                reservado = item.insumo_id.reservado - item.monto
                comprometido = item.insumo_id.comprometido + item.monto
                item.insumo_id.write({'reservado': reservado, 'comprometido': comprometido})



    _order = 'create_date desc'

class purchaseRequisicionLine(models.Model):
    _name = 'purchase.order.requisition.line'

    actividad_id = fields.Many2one('planificacion.actividad_producto_resultado', string='Actividad')
    employee_id = fields.Many2one('hr.employee', string='Responsable Actividad')
    insumo_id = fields.Many2one('planificacion.actividad_producto_resultado_detalle', string='Insumo')

    @api.onchange('monto', 'disponible')
    def change_value(self):
        if self.monto > self.disponible:
            self.monto = 0.0
            return {'warning': {'title': 'Error!', 'message': 'El monto ingresado supera el monto disponible'}}

    @api.depends('requisition_id.program_id')
    def _default_program(self):
        if self.requisition_id.program_id:
           self.program_id = self.requisition_id.program_id.id

    program_id = fields.Many2one(comodel_name='budget.program', string='Fuente de financiamiento', compute='_default_program', store=True, readonly=True)
    presupuesto_id = fields.Many2one(comodel_name='budget.program_detail', string='Presupuesto de proyecto')

    # ('program_id', 'in', [g.fuenteFinanciamiento for g in planificacion.actividad_producto_resultado_detalle])]

    @api.depends('insumo_id')
    def _compute_name(self):
        if self.insumo_id:
            self.monto_asignado = self.insumo_id.montoAsignado
            self.disponible = self.insumo_id.disponible


    monto = fields.Float(string='Monto Utilizar')
    disponible = fields.Float(string='Monto Disponible', compute='_compute_name', store=True, readonly=True)
    monto_asignado = fields.Float(string='Monto Asignado', compute='_compute_name', store=True, readonly=True)

    @api.onchange('insumo_id')
    def onchange_program(self):
        # corre_this = self.env['purchase.sequences'].search([('program_id', '=', self.program_id.id)])
        if self.insumo_id:
            self.program_id = self.insumo_id.fuenteFinanciamiento.id
            self.presupuesto_id = self.insumo_id.detalleFuenteFinanciamiento.id

    # codigo_actividad = fields.Char(string='Código actividad')
    # name = fields.Text(string='Nombre de actividad')
    # insumo = fields.Many2one(comodel_name='budget.line', string='Insumo')
    # fuente_financiamiento = fields.Many2one(comodel_name='budget.program', string='Fuente de financiamiento')
    # detalle_fuente_financiamiento = fields.Many2one(comodel_name='budget.program_detail',
    #                                               string='Presupuesto de proyecto')
    # monto_fuente_financiamiento = fields.Float(string='Monto disponible')
    # monto_asignado = fields.Float(string='Monto asignado')
    requisition_id = fields.Many2one('purchase.order.requisitions', 'id Linea')

class purchaseOrderDocs(models.Model):
    _name = 'purchase.order.docs'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Many2one('purchase.type.doc', 'Tipo de Documento')
    namefile = fields.Binary('Nombre Archivo')
    files = fields.Binary('Archivos')
    description = fields.Text('Comentario')
    requisition_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')

    filename_adjunto = fields.Char(string='Nombre Archivo')
    file_adjunto = fields.Binary('Archivo')

class purchaseOrderAutorizaciones(models.Model):
    _name = 'purchase.order.autorizacion'

    name = fields.Char('Accion')
    type = fields.Selection([('creacion', 'Creacion'),
                             ('auto', 'Autorizacion'),
                             ('auto_com', 'Autorizacion Compras')], 'Tipo')
    user_id = fields.Many2one('res.users', 'Usuario')
    date_acc = fields.Datetime('Fecha')
    requisition_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')

class purchaseLineRequisicion(models.Model):
    _name = 'purchase.line.requisicion'

    name = fields.Many2one('res.partner', 'Proveedor')
    # Calculo final de los detalles de la adjudicacion

    @api.depends('lines_ids', 'lines_ids.monto_adjudicado')
    def _compute_detalle(self):
        monto = 0.0
        for items in self.lines_ids:
            monto += items.monto_adjudicado

        self.monto = monto

    @api.depends('lines_ids', 'lines_ids.monto_pre')
    def _compute_monto_pre(self):
        monto = 0.0
        for items in self.lines_ids:
            monto += items.monto_pre

        self.monto_pre = monto

    monto = fields.Float(string='Monto adjudicado  ', store=True, readonly=True,
                                      compute=_compute_detalle)

    monto_pre = fields.Float(string='Monto presupuestado  ', store=True, readonly=True,
                                      compute=_compute_monto_pre)

    requisition_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')
    lines_ids = fields.One2many('purchase.lines.requisicion', 'lines_ids', string='Lineas de adjudicacion')

    def WizardEnviarNotificacion(self, id_transfer):
        view = self.env.ref('toff.bolpros_ofertas_notificacion_form_view')
        context = dict(self.env.context)
        context.update({'default_name': self.partner_id})
        return {
            'name': _('Enviar Notificaciones'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account_move',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    @api.onchange('requisition_id')
    def _onchange_obtener_proveedor(self):
        for rec in self:
            return {'domain': {'name': [('id', 'in', rec.requisition_id.lineas_oferta_ids.name.ids)]}}


class purchaseLineRequisicion(models.Model):
    _name = 'purchase.lines.requisicion'

    @api.onchange('lines_ids','cantidad', 'price_unitary', 'price_unitary_ad')
    def _onchange_patient_card(self):
        for rec in self:
            return {'domain': {'insumo_id': [('id', 'in', rec.lines_ids.requisition_id.purchase_requi_line_ids.insumo_id.ids)]}}


    @api.depends('cantidad','price_unitary')
    def _computemonto_pre(self):
        for record in self:
            record.monto_pre =record.cantidad * record.price_unitary

    @api.depends('cantidad', 'price_unitary_ad')
    def _computemonto_adj(self):
        for record in self:
            record.monto_adjudicado = record.cantidad * record.price_unitary_ad

    name = fields.Text('Descripcion')
    cantidad = fields.Float('cantidad', default=1.00)
    price_unitary = fields.Float('Prec. Unit Presupuesto', default=0.00 )
    monto_pre = fields.Float(string='Monto Presupuesto', default=0.00, compute='_computemonto_pre')
    price_unitary_ad = fields.Float('Prec. Unit Adjudicado', default=0.00 )
    monto_adjudicado = fields.Float(string='Monto Adjudicado', default=0.00, compute='_computemonto_adj')
    adjudication = fields.Boolean('Adjudicacion')
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)], change_default=True)
    insumo_id = fields.Many2one('planificacion.actividad_producto_resultado_detalle', string='Insumo')
    lines_ids = fields.Many2one('purchase.line.requisicion', 'Lineas de requisicion')

class purchaseLineRequisicionAdjudicacion(models.Model):
    _name = 'purchase.line.requisicion.adjudicacion'

    name = fields.Many2one('res.partner', 'Proveedor')
    monto_ad = fields.Float('Monto Adjudicado')
    adjudicacion_ids = fields.Many2one('purchase.order.requisitions', 'Lineas de adjudicacion')
    date_order = fields.Date('Fecha de adjudicación')
    det_adjudicacion_ids = fields.One2many('purchase.requisicion.line', 'det_adjudicacion_ids', string='Lineas de adjudicacion')


class purchaseLineRequisicionAdjudicacionLine(models.Model):
    _name = 'purchase.requisicion.line'

    name = fields.Text('Descripcion')
    monto_linea = fields.Float('Monto Adjudicado')
    det_adjudicacion_ids = fields.Many2one('purchase.line.requisicion.adjudicacion', 'Lineas de adjudicacion')

class Contrato(models.Model):
    _name = 'purchase.order.requisitions.contrato'

    name = fields.Integer('Número de Contrato')
    nombre_contrato = fields.Text('Nombre del contrato')
    proveedor_id = fields.Many2one('purchase.line.requisicion.adjudicacion', 'Proveedor')
    fecha_firma = fields.Date('Firma de contrato')
    fecha_inicio = fields.Date('Inicio')
    fecha_finalizacion =  fields.Date('Desde')
    plazo = fields.Text(string='Plazo')
    monto = fields.Float(string='Monto')
    producto =  fields.Text(string='Productos')
    plan_pagos = fields.Text(string='Plan de pagos')
    fianza_fiel = fields.Boolean(string='Fianza de fiel cumplimiento')
    fecha_entrega = fields.Date('Fecha de entrega')
    adjunto = fields.Binary('Contrato adjunto')
    contrato_ids = fields.Many2one('purchase.order.requisitions', string='Contrato')

    @api.onchange('contrato_ids')
    def _onchange_obtener_proveedor(self):
        for rec in self:
            return {'domain': {'proveedor_id': [('id', 'in', rec.contrato_ids.adjudicacion_ids.ids)]}}

    @api.onchange('proveedor_id')
    def _onchange_name(self):
        if self.proveedor_id:
            self.monto = self.proveedor_id.monto_ad
            self.producto = self.proveedor_id.det_adjudicacion_ids.name





class purchaseorderOfertas(models.Model):
    _name = 'purchase.order.ofertas'

    ##name = fields.Char('Documento')

    name = fields.Many2one('res.partner')

    archivo = fields.Binary('Archivo')
    description = fields.Text('Descripcion')
    date_reception = fields.Date('Fecha de Recepcion')
    requisition_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')

class pucharseOrderAdjudicacion(models.Model):
    _name = 'purchase.order.adjudicacion'

    name = fields.Many2one('res.partner')
    date_envio = fields.Date('Fecha de Envio')
    observation = fields.Text('Observaciones')
    adjudication = fields.Boolean('Adjudicacion')
    date_adjudication = fields.Date('Fecha de Adjudicacion')
    requisition_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')
    lineas_adjudicacion = fields.Many2many('purchase.line.requisicion', 'rel_lineas_requisiciones', 'adjudicacion_id',
                                           'detalle_id', 'Productos Adjudicados')

class purchaseOrderService(models.Model):
    _name = 'purchase.order.service'

    clase = fields.Many2one('order.service.clase', 'Clase')
    name = fields.Char('Nombre')
    proveedor = fields.Many2one('res.partner', 'Proveedor')
    objetivo_general = fields.Text('Objetivo General')
    desde = fields.Date('Desde')
    hasta = fields.Date('Hasta')
    cordinacion = fields.Text('COORDINACIÓN')
    terminacion = fields.Text('TERMINACIÓN')
    product_id = fields.Many2one('product.product', 'Actividad')
    lineas_ids = fields.One2many('purchase.order.service.line', 'order_id', 'Lineas de Actividad')
    precios_formas_ids = fields.One2many('purchase.order.forma.pago', 'orden_id', 'Formas de Pago')
    requisicion_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')

class purchaseorderServiceLine(models.Model):
    _name = 'purchase.order.service.line'

    name = fields.Many2one('product.service', 'Producto')
    order_id = fields.Many2one('purchase.order.service', 'Orden de Servicio')

class purchaseFormaPago(models.Model):
    _name = 'purchase.order.forma.pago'

    name = fields.Text('Descripción')
    precio = fields.Float('Precio')
    numero = fields.Integer('Numero de Pago')
    orden_id = fields.Many2one('purchase.order.service', 'Orden de Servicio')

class orderServiceClase(models.Model):
    _name = 'order.service.clase'
    
    name = fields.Char('Nombre Clase')

class serviceproduct(models.Model):
    _name = 'product.service'

    name = fields.Char('Nombre')
    codigo = fields.Char('Codigo')

class Evaluaciones(models.Model):
    _name = 'purchase.order.evaluacion'

    name = fields.Integer('Correlativo')
    criterio_id = fields.Many2one('purchase.order.evaluacion.criterio', string='Criterio')
    indicador = fields.Text('Detalle de Indicador')
    valor1 = fields.Float(string='Valor 1')
    valor2 = fields.Float(string='Valor 2')





    order_id = fields.Many2one('purchase.order.requisitions', string='Requisicion')

class EvaluacionesTipo(models.Model):
    _name = 'purchase.order.evaluacion.criterio'

    name = fields.Char('Nombre')


## Cambio en el modelo para las evaluaciones
class ComiteEvaluaciones(models.Model):
     _name = 'purchase.order.comite.evaluacion'

     name = fields.Many2one('purchase.order.evaluacion.criterio.evaluaciones', string='Criterio')
     puntaje_total = fields.Float(string='Puntaje')
     order_id = fields.Many2one('purchase.order.requisitions', string='Requisicion')

     @api.onchange('formacion_academica')
     def change_value(self):
         if self.formacion_academica == 'titulo':
             self.puntaje_conocimiento = 0.0
             self.puntaje_conocimiento += 20.0

         if self.formacion_academica == 'similar':
             self.puntaje_conocimiento = 0.0
             self.puntaje_conocimiento += 10.0

         if self.formacion_academica == 'tecnico':
             self.puntaje_conocimiento = 0.0
             self.puntaje_conocimiento += 5.0



     @api.onchange('trabajos_anteriores')
     def change_value1(self):
         if self.trabajos_anteriores == '1':
             self.puntaje_experiencia = 0.0
             self.puntaje_experiencia += 20.0

         if self.trabajos_anteriores == '2':
             self.puntaje_experiencia = 0.0
             self.puntaje_experiencia += 10.0

         if self.trabajos_anteriores == '3':
             self.puntaje_experiencia = 0.0
             self.puntaje_experiencia += 5.0



     @api.onchange('Propuesta_tecnica')
     def change_value2(self):
         if self.Propuesta_tecnica == '1':
             self.puntaje_capacidad = 0.0
             self.puntaje_capacidad += 30.0

         if self.Propuesta_tecnica == '2':
             self.puntaje_capacidad = 0.0
             self.puntaje_capacidad += 20.0

         if self.Propuesta_tecnica == '3':
             self.puntaje_capacidad = 0.0

     @api.onchange('plan_trabajo')
     def change_value3(self):
         if self.plan_trabajo == '1':
             self.puntaje_capacidad = self.puntaje_capacidad + 15.0

     @api.onchange('cronograma')
     def change_value4(self):
         if self.cronograma == '1':
             self.puntaje_capacidad = self.puntaje_capacidad + 15.0

         if self.puntaje_capacidad > 60:
             self.puntaje_capacidad = 60.00



     @api.onchange('puntaje_conocimiento','puntaje_capacidad','puntaje_experiencia')
     def change_valuetotal(self):
         self.puntaje_total = self.puntaje_conocimiento + self.puntaje_capacidad + self.puntaje_experiencia

     # (A) Conocimiento

     puntaje_conocimiento = fields.Float(string='Puntaje')
     formacion_academica = fields.Selection([('titulo', 'Titulo'),
                                             ('similar', 'Similar'),
                                             ('tecnico', 'Técnico')], 'Formación académica')

     # (B) Experiencia
     puntaje_experiencia = fields.Float(string='Puntaje')
     trabajos_anteriores = fields.Selection([('1', 'Más de 3 años'),
                                             ('2', '3 años'),
                                             ('3', 'Menos de 3 años')], 'Trabajos anteriores')

     # (B) Capacidad

     puntaje_capacidad = fields.Float(string='Puntaje')
     Propuesta_tecnica = fields.Selection([('1', 'Metodología supera la expectativa'),
                                             ('2', 'Metodología cumple con los solicitado'),
                                             ('3', 'Metodología no cumple lo solicitado')], 'Propuesta técnica')

     plan_trabajo = fields.Selection([('1', 'Plan de trabajo cumple'),
                                             ('2', 'Plan de trabajo no cumple')], 'Plan de trabajo')

     cronograma = fields.Selection([('1', 'Cronograma de actividades adecuado')], 'Cronograma')





class CriteriosEvaluaciones(models.Model):
        _name = 'purchase.order.evaluacion.criterio.evaluaciones'

        name = fields.Char('Nombre')

#Acá finaliza

#Desde aca se definen los modelos para los informes
#Se crea un modelo y se crea un campo
#
class InformeInsumo(models.Model):
    _name = 'purchase.order.requisitions.informe.insumo'

    name = fields.Char(string='Nombre')

class InformeFinanciamiento(models.Model):
    _name = 'purchase.order.requisitions.informe.financiamiento'

    name = fields.Char(string='Nombre')

class InformeProveedores(models.Model):
    _name = 'purchase.order.requisitions.informe.proveedores'

    name = fields.Char(string='Nombre')


class InformeActividad(models.Model):
    _name = 'purchase.order.requisitions.informe.actividad'

    name = fields.Char(string='Nombre')


class InformePlanProyecto(models.Model):
    _name = 'purchase.order.requisitions.informe.planproyecto'

    name = fields.Char(string='Nombre')


class InformePorCodigo(models.Model):
    _name = 'purchase.order.requisitions.informe.porcodigo'

    name = fields.Char(string='Nombre')


class InformeComprasFuente(models.Model):
    _name = 'purchase.order.requisitions.informe.comprasfuente'

    name = fields.Char(string='Nombre')


class InformePresupuestoTrimestral(models.Model):
    _name = 'purchase.order.requisitions.informe.presupuestotrimestral'

    name = fields.Char(string='Nombre')


