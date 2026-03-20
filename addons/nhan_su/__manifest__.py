# -*- coding: utf-8 -*-
{
    'name': "nhan_su",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    # 'depends': ['base'],
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'views/hr_employee_views.xml',
        # 'security/ir.model.access.csv',
        # 'views/chuc_vu.xml',
        # 'views/don_vi.xml',
        # 'views/nhan_vien.xml',
        'views/nhan_su_dashboard.xml',
        'views/menu.xml',
    ],
    
    'demo': [
        'demo/demo_nhan_su.xml',
    ],

    'pre_init_hook': 'pre_init_hook',
}
