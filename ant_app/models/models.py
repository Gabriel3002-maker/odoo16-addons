# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests


class Conductores(models.Model):
    _name = "ant_app.conductores"
    _description = "conductores"

    name = fields.Char(string='Nombre', required=True)
    phone = fields.Char(string='Telefono', required=True)
    password = fields.Char(string='Contraseña', required=True)
    email = fields.Char(string='Email')
    work_contact_id = fields.Char(string='Id_Contacto')
    idRole = fields.Char(string='IdRole')
    id_odoo = fields.Char(string='Id_Odoo')
    state = fields.Char(string='state')
    type = fields.Char(string='type')

    # Obtener el correo
    @api.model
    def _get_work_email(self):
        employees = self.env['hr.employee'].search([])
        return [(employee.id, employee.work_email) for employee in employees]

    work_email = fields.Selection(selection="_get_work_email", string="Buscador", widget="selection", options="_get_work_email")




    @api.onchange("work_email")
    def onchange_email(self):
        if self.work_email:
            # Obten el nombre asociado al ID seleccionado en work_email
            employee = self.env['hr.employee'].browse(self.work_email)
            if employee:
                self.email = employee.work_email
                self.name = employee.name
                self.phone = employee.work_phone
                self.work_contact_id = employee.work_contact_id
                print(f"Nombre: {self.name}")
                print(f"Teléfono: {self.phone}")
                print(f"work_contact_id: {self.work_contact_id}")

    def send_data_to_endpoint(self):
         # Aquí construye los datos que deseas enviar al endpoint
         data_to_send = {
              'name': self.name,
              'email': self.email,
              'phone': self.phone,
              'idRole': self.idRole,
              'user': self.email,
              'password': self.password,
              'state': self.state,
              'id_odoo': self.id_odoo,
              'type': self.type
         }

         # Define la URL del endpoint
         endpoint_url = 'https://ant-kurier.backend.chvconsulting.es/account/create'

         # Envia la solicitud HTTP POST al endpoint con los datos
         response = requests.post(endpoint_url, json=data_to_send)

         # Maneja la respuesta según sea necesario
         if response.status_code == 201:
              # Registro exitoso
              self.popupNotification(title="Felicidades", message="Registrado en la APP-MOVIL")

         elif response.status_code == 400:
              # Correo ya registrado
              self.popupNotification(title="Error de Registro", message="Correo ya registrado")
         elif response.status_code == 500:
              # Campos incompletos
              self.popupNotification(title="Error de Registro", message="Campos Incompletos")

         else:
              # Otro error
              self.popupNotification(title="Error de Registro", message="Error en el servidor")

    def popupNotification(self, title, message, notification_type="info"):
        self.env['bus.bus']._sendone(self.env.user.partner_id,
                                     "simple_notification",
                                     {
                                         "title": title,
                                         "message": message,
                                         "type": notification_type,
                                     })
        return True