# -*- coding: utf-8 -*-
# from odoo import http


# class ./new-addons/new-addons/terceros/odoo16-addons/antApp(http.Controller):
#     @http.route('/./new-addons/new-addons/terceros/odoo16-addons/ant_app/./new-addons/new-addons/terceros/odoo16-addons/ant_app', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./new-addons/new-addons/terceros/odoo16-addons/ant_app/./new-addons/new-addons/terceros/odoo16-addons/ant_app/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('./new-addons/new-addons/terceros/odoo16-addons/ant_app.listing', {
#             'root': '/./new-addons/new-addons/terceros/odoo16-addons/ant_app/./new-addons/new-addons/terceros/odoo16-addons/ant_app',
#             'objects': http.request.env['./new-addons/new-addons/terceros/odoo16-addons/ant_app../new-addons/new-addons/terceros/odoo16-addons/ant_app'].search([]),
#         })

#     @http.route('/./new-addons/new-addons/terceros/odoo16-addons/ant_app/./new-addons/new-addons/terceros/odoo16-addons/ant_app/objects/<model("./new-addons/new-addons/terceros/odoo16-addons/ant_app../new-addons/new-addons/terceros/odoo16-addons/ant_app"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./new-addons/new-addons/terceros/odoo16-addons/ant_app.object', {
#             'object': obj
#         })
