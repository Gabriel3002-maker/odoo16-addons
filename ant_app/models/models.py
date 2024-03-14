# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import re


class Conductores(models.Model):
    _name = "ant_app.conductores"
    _description = "conductores"

    # Account
    name = fields.Char(string='Nombre', required=True)
    phone = fields.Char(string='Telefono', required=True)
    password = fields.Char(string='Contraseña', required=True, widget='password')
    email = fields.Char(string='Email')
    work_contact_id = fields.Char(string='Id_Contacto')
    idrole = fields.Selection([
        ('1', 'Conductor'),
        ('2', 'Administrativo'),
        ('3', 'Secretariado')
    ], string='Rol')

    state = fields.Char(string='state', default='1')
    # vehicle
    id_odoo = fields.Char(string='Id Odoo')
    model = fields.Char(string='Modelo')
    plac = fields.Char(string='Placa')
    id_veh = fields.Char(string='Id Vehiculo')
    odometer = fields.Char(string='Odometro')

    # Obtener el correo
    @api.model
    def _get_work_email(self):
        employees = self.env['hr.employee'].search([])
        return [(employee.id, employee.work_email) for employee in employees]

    work_email = fields.Selection(selection="_get_work_email", string="Buscador", widget="selection",
                                  options="_get_work_email")

    @api.onchange("work_email")
    def onchange_email(self):
        if self.work_email:
            print('ID empleado:', self.id)
            # Obten el nombre asociado al ID seleccionado en work_email
            employee = self.env['hr.employee'].browse(self.work_email)
            if employee:
                self.email = employee.work_email
                self.name = employee.name
                self.phone = employee.work_phone
                self.work_contact_id = employee.work_contact_id
                self.id_odoo = employee.id
                print(f"Nombre: {self.name}")
                print(f"Teléfono: {self.phone}")
                print(f"work_contact_id: {self.work_contact_id}")
                print(f"id: {self.id_odoo}")


                try:
                    match = re.search(r'\((\d+),\)', self.work_contact_id)
                    if match:
                        driver_id = int(match.group(1))
                        print(f'Valor numérico de work_contact_id: {driver_id}')
                        self.work_contact_id = driver_id
                        # Realizar la búsqueda en el modelo 'fleet.vehicle'
                        fleet_vehicle_records = self.env['fleet.vehicle'].search([('driver_id', '=', driver_id)])

                        # Puedes acceder a los registros obtenidos, por ejemplo, iterando sobre ellos
                        for fleet_vehicle in fleet_vehicle_records:
                            # Mostrar información sobre el objeto fleet_vehicle
                            print(f"Objeto fleet_vehicle: {fleet_vehicle}")

                            # Verificar si el campo 'model_id' está presente en el objeto
                            if hasattr(fleet_vehicle, 'model_id'):
                                # Acceder al campo 'model_id' para obtener el modelo del vehículo
                                self.model = fleet_vehicle.model_id.name
                                self.plac = fleet_vehicle.license_plate
                                self.id_veh = fleet_vehicle.id
                                print(f"Modelo del vehículo: {self.model}")
                                print(f"Placa del vehículo: {self.plac}")
                                print(f"ID Vehiculo: {self.id_veh}")

                                #Buscamos nuestro odooetro con el id_veh
                                fleet_vehicle_odometer = self.env['fleet.vehicle.odometer'].search(
                                    [('vehicle_id', '=', fleet_vehicle.id)])

                                #Ordenamos los registros por Fecha Descendete
                                sorted_odometer_records = sorted(fleet_vehicle_odometer, key=lambda x:x.date, reverse=True)
                                if sorted_odometer_records:
                                    last_odometer_record = sorted_odometer_records[0]
                                    print('Ultimo odometro del vehiculo', last_odometer_record)
                                    #Asfgnar
                                    self.odometer = last_odometer_record.value
                                else:
                                    print('No se Encontraron Registros')


                            else:
                                print("El campo 'model_id' no está presente en el objeto fleet_vehicle.")

                        # Verificar si se encontraron vehículos para el conductor
                        if not fleet_vehicle_records:
                            print("No se encontraron vehículos para el conductor.")
                    else:
                        print("No se pudo extraer el ID de work_contact_id.")

                except Exception as e:
                    print(f"Error en la búsqueda de fleet.vehicle: {e}")

    # Enviar Data
    def send_data_to_endpoint(self):
        # Aquí construye los datos que deseas enviar al endpoint
        data_to_send = {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'idRole': int(self.idrole),
            'user': self.email,
            'password': self.password,
            'state': self.state,
            'id_odoo': self.id_odoo,
            'model': self.model,
            'placa': self.plac,
            "idVehicle_odoo": self.id_veh,
            "odometer_odoo": self.odometer,
        }

        print('json a enviar', data_to_send)

        # Define la URL del endpoint
        endpoint_url = 'https://ant-kurier.backend.chvconsulting.es/account/create'

        # Envia la solicitud HTTP POST al endpoint con los datos
        response = requests.post(endpoint_url, json=data_to_send)

        # Maneja la respuesta según sea necesario
        if response.status_code == 201:
            # Registro exitoso
            return self.open_wizard(title="Felicidades", message="Registrado en la APP-MOVIL", success=True)

        elif response.status_code == 400:
            # Correo ya registrado
            return self.open_wizard(title="Error de Registro", message="Correo ya registrado", success=False)
        elif response.status_code == 500:
            # Campos incompletos
            return self.open_wizard(title="Error de Registro", message="Campos Incompletos", success=False)

        else:
            # Otro error
            return self.open_wizard(title="Error de Registro", message="Error en el servidor", success=False)

    def popupNotification(self, title, message, notification_type="info"):
        self.env['bus.bus']._sendone(self.env.user.partner_id,
                                     "simple_notification",
                                     {
                                         "title": title,
                                         "message": message,
                                         "type": notification_type,
                                     })
        return True
    
    def open_wizard(self, title, message, success):
        return {
            'name': title,
            'type': 'ir.actions.act_window',
            'res_model': 'ant.app.message.wizard',
            'context': {
                'default_message': message,
                'default_success': success
                },
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }