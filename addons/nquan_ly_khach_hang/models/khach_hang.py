from odoo import models, fields

class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = "Khách hàng"
    _rec_name = "ma_kh"
    
    ten_kh = fields.Char(string='Tên khách hàng', required=True)
    email = fields.Char(string='Địa chỉ email')
    sdt = fields.Char(string='Số điện thoại', required=True)
    dia_chi = fields.Text(string="Địa chỉ khách hàng", required=True)
    ma_kh = fields.Char(string="Mã khách hàng", required=True)
    loai_kh = fields.Selection(
        [('ca_nhan', 'Cá nhân'), ('doanh_nghiep', 'Doanh nghiệp')],
        string="Loại khách hàng",
        default='doanh_nghiep', required=True
    )
    ma_so_thue = fields.Char(string="Mã số thuế")
    ghi_chu = fields.Text(string="Ghi chú")
