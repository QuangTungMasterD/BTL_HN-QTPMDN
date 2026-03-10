from odoo import models, fields

class NhanVienThamGia(models.Model):
    _name = 'nhan_vien_tham_gia'
    _description = 'Nhân viên tham gia'
    _rec_name = "du_an_id"

    du_an_id = fields.Many2one(
        'du_an',
        string='Dự án tham gia',
        required=True
    )

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên',
        required=True
    )

    vai_tro = fields.Char(string='Vai trò')
