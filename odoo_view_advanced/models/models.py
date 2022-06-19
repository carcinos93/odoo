# -*- coding: utf-8 -*-
import io
import base64
from odoo import models, fields, api, exceptions


class CustomItem(models.Model):
    _name = 'odoo_view_advanced.custom_item'

    name = fields.Char(string='Descripción')
    unit_price = fields.Char(string='Precio unitario')

    properties = fields.One2many(comodel_name='odoo_view_advanced.property',inverse_name='custom_item_ids',string='Propiedades', required=False)

    def removeItems(self, user):
        print('Borrando items...' )
        print(user)
        return True


    def save_update(self):
       if self.id:
           super().write( self )
       else:
           super().create(self)

class Property(models.Model):
    _name = 'odoo_view_advanced.property'

    name = fields.Char(string='Propiedad')
    value = fields.Char(string='Valor')
    custom_item_ids = fields.Many2one(comodel_name='odoo_view_advanced.custom_item',string='Custom_item_ids', required=False, ondelete='cascade')

class UploadFile(models.TransientModel):
    _name = 'odoo_view_advanced.upload_file'

    upload_file = fields.Binary(string='Subir fichero', required=True)
    file_name = fields.Char(string='Nombre del fichero')

    def import_file(self):
        if self.file_name:
            if '.csv' not in self.file_name:
                raise exceptions.ValidationError('El archivo debe ser un CSV')
            file = self.read_file_from_binary(self.upload_file)
            lines = file.split('\n')
            for line in lines:
                elements = line.split(';')
                if len(elements) > 1:
                    self.env['odoo_view_advanced.custom_item'].create({
                        'name': elements[0],
                        'unit_price': float(elements[1])
                    })

    def read_file_from_binary(self, file):
        try:
            with io.BytesIO(base64.b64decode(file)) as f:
                f.seek(0)
                return f.read().decode('UTF-8')
        except Exception as e:
            print(str(e))
            raise e



class ResPartner(models.Model):
    _inherit = 'res.partner'
    customer_rank = fields.Integer(string='Customer rank', default=1)

    def getItems(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Productos',
            'view_mode': 'tree,form',
            'res_model': 'odoo_view_advanced.custom_item',

        }
    #'domain': [(...)], Filtrar
    # 'context': '{"create": False}' Permitir a acciones