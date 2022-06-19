from odoo import fields, models, api


class Dummy(models.Model):
    _name = 'planificacion.dummy'
    _description = 'Description'

    def cargar_formulario(self):
        form = self._context.get('form')
        tree = self._context.get('tree')
        title = self._context.get('title')
        model = self._context.get('model')
        act_window = self._context.get('act_window')

        modulo = "i10n_sv_planificacion"
        formRef = self.env.ref( "%s.i10n_sv_planificacion_%s" % ( modulo, form  )  )
        treeRef = self.env.ref( "%s.i10n_sv_planificacion_%s" % ( modulo, tree  )  )

        #actWindowRef = self.env.ref("%s.i10n_sv_planificacion_%s" % ( modulo, act_window ))

        rec = self.env['ir.actions.act_window']._for_xml_id("%s.i10n_sv_planificacion_%s" % ( modulo, act_window ))

        return {
            'name': title,
            'view_mode': 'tree',
            'views': [[treeRef.id, 'tree'], [formRef.id, 'form']],
            'res_model':  'planificacion.%s' % model ,
            'type': 'ir.actions.act_window',
            'domain': rec['domain'],
            'context': rec['context'],
            'target': 'current',
        }