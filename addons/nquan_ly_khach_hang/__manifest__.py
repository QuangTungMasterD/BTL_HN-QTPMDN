# -*- coding: utf-8 -*-
{
    'name': "nquan_ly_khach_hang",

    'summary': "Quản lý khách hàng, lịch hẹn, tương tác và đánh giá",

    'description': """
Module quản lý khách hàng cho công ty xây dựng: thông tin khách hàng, lịch hẹn,
tương tác và đánh giá gắn với dự án.
    """,

    'author': "Student",
    'website': "http://www.example.com",

    'category': 'Sales/CRM',
    'version': '0.1',

    'depends': ['base', 'nhan_su'],
    'assets': {
        'web.assets_backend': [
            'nquan_ly_khach_hang/static/src/css/khach_hang.css',
        ],
    },

    'data': [
        'security/ir.model.access.csv',
        'views/khach_hang.xml',
        'views/lich_hen.xml',
        'views/tuong_tac.xml',
        'views/danh_gia.xml',
        'views/khach_hang_dashboard.xml',
        # 'data/email_templates.xml',
        'views/menu.xml',
    ],

    'demo': [
        'demo/demo_khach_hang.xml',
    ],
}

