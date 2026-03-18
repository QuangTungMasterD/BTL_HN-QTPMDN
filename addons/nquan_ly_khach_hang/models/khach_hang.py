from odoo import models, fields, api
from odoo.exceptions import ValidationError

class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = "Khách hàng"
    _rec_name = "ma_kh"
    
    ma_kh = fields.Char(string="Mã khách hàng", required=True)
    ten_kh = fields.Char(string='Tên khách hàng', required=True)
    email = fields.Char(string='Địa chỉ email', required=True)
    sdt = fields.Char(string='Số điện thoại', required=True)
    dia_chi = fields.Text(string="Địa chỉ khách hàng", required=True)
    loai_kh = fields.Selection(
        [('ca_nhan', 'Cá nhân'), ('doanh_nghiep', 'Doanh nghiệp')],
        string="Loại khách hàng",
        default='doanh_nghiep', required=True
    )
    ma_so_thue = fields.Char(string="Mã số thuế")
    ghi_chu = fields.Text(string="Ghi chú")

    _sql_constraints = [
        ('ma_kh_unique', 'unique(ma_kh)', 'Mã khách hàng đã tồn tại!')
    ]

    @api.constrains('ma_kh')
    def _check_ma_kh(self):
        for rec in self:
            if self.search_count([
                ('ma_kh', '=', rec.ma_kh),
                ('id', '!=', rec.id)
            ]) > 0:
                raise ValidationError("Mã khách hàng đã tồn tại!")
