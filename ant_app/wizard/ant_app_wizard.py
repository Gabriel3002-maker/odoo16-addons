from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class RequestChangeWizard(models.TransientModel):
    _name = 'ant.app.message.wizard'
    _description = "Message successfull wizard"

    message = fields.Char(string=_('Message'))
    title = fields.Char(string=_('success'))
    success = fields.Boolean(string=_('success'), default=False)


    def confirm(self):
        action = {
            'name': 'Ant conductores',
            'type': 'ir.actions.act_window',
            'res_model': "ant_app.conductores",
            'view_mode': 'tree,form',
        }
        return action