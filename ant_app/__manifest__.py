# -*- coding: utf-8 -*-
{
    'name': "ANT APP DRIVERS",
    'summary': """ANT REGISTER USER FOR APP MOVIL""",

    'description': """
       ANT REGISTER USER FOR APP MOVIL
    """,

    'author': "CHVConsulting",
    'website': "https://chvconsulting.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'tecnico',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/ant_app_wizard.xml'
    ],
}
