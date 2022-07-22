from odoo import fields, models, api, exceptions
import io
import base64

class UploadFile(models.Model):
    _name = 'libro_modulo.upload_file'
    _description = 'Description'

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
                    self.env['libro_modulo.libro'].create({
                        'titulo': elements[0],
                        'descripcion': elements[1],
                        'precio': float(elements[2])
                    })

    def read_file_from_binary(self, file):
        try:
            with io.BytesIO(base64.b64decode(file)) as f:
                f.seek(0)
                return f.read().decode('UTF-8')
        except Exception as e:
            print(str(e))
            raise e
