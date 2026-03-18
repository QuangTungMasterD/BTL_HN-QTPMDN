# -*- coding: utf-8 -*-
{
    'name': "nquan_ly_du_an",

    'summary': "Quản lý dự án",

    'description': """
        Module quản lý dự án cho công ty phần mềm: thông tin dự án, khách hàng.
    """,

    'author': "Student",
    'website': "http://www.example.com",

    'category': 'Sales/CRM',
    'version': '0.1',

    'depends': ['base', 'nhan_su', 'nquan_ly_khach_hang', 'base_automation', 'mail'],
    'assets': {
        'web.assets_backend': [
            'nquan_ly_khach_hang/static/src/css/khach_hang.css',
        ],
    },

    'data': [
        'security/ir.model.access.csv',
        'views/du_an.xml',
        'views/kinh_phi_du_kien.xml',
        'views/nhan_vien_tham_gia.xml',
        'views/bao_cao_tien_do_du_an.xml',
        'views/du_an_dashboard.xml',
        'data/automation/01_create_tasks_on_project.xml',
        'data/automation/02_assign_project_manager.xml',
        'data/templates/email_deadline_project_templates.xml',
        'data/automation/project_deadline_reminder.xml',
        'views/menu.xml',
    ],

    'demo': [
        'demo/demo_du_an.xml',
    ],
}

