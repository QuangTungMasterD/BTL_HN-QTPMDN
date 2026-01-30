# -*- coding: utf-8 -*-
{
    'name': "nquan_ly_cong_viec",

    'summary': "Quản lý dự án và công việc cho công ty xây dựng",

    'description': """
Quản lý dự án, công việc, kinh phí dự kiến, nhân viên tham gia và báo cáo tiến độ.
    """,

    'author': "Student",
    'website': "http://www.example.com",

    'category': 'Project',
    'version': '0.1',

    'depends': ['base', 'nhan_su', 'nquan_ly_khach_hang'],

    'data': [
        'security/ir.model.access.csv',
        'views/du_an.xml',
        'views/cong_viec.xml',
        'views/bao_cao_tien_do.xml',
        'views/kinh_phi_du_kien.xml',
        'views/nhan_vien_tham_gia.xml',
        'views/menu.xml',
    ],
}

