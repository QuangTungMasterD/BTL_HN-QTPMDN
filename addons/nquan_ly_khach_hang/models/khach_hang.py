from odoo import models, fields

class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = "Khách hàng"
    
    ten_kh = fields.Char(string='Tên khách hàng', required=True)
    email = fields.Char(string='Địa chỉ email')
    sdt = fields.Char(string='Số điện thoại', required=True)
    dia_chi = fields.Text(string="Địa chỉ khách hàng", required=True)
