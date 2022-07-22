from odoo import fields, models, api


class Factura(models.Model):
    _name = 'libro_modulo.factura'
    _description = 'Factura de libros'
    _rec_name = 'noFactura'

    @api.depends('detalles', 'detalles.precio')
    def _group_detail(self):
        for record in self:
            html = "<table class='table table-bordered w-100'>"
            data = {}
            for item in record.detalles:
                if data.get(item.categoria1, "no") == "no":
                    data[item.categoria1] = 0
                data[item.categoria1] = data[item.categoria1] + item.precio
            for key in data:
                html += "<tr> <td> %s </td> <td> %s </td> </tr>" % (key, data[key])
            html += "</table>"
            record.html = html

    noFactura = fields.Char(string='No factura', required=False)
    nombreDe = fields.Char(string='Nombre de', required=False)
    fecha = fields.Date(string='Fecha', required=False)
    descripcion = fields.Text(string="Descripcion", required=False)
    detalles = fields.One2many(comodel_name='libro_modulo.factura_detalle', inverse_name='factura_ids',
                               string='Detalles', required=False)
    html = fields.Text(string="Html", required=False, compute=_group_detail, store=True)
