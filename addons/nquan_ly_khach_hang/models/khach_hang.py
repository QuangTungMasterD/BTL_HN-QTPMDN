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

    @api.model
    def create(self, vals):
        if 'ma_kh' not in vals:
            vals['ma_kh'] = self._generate_code('KH', 'ma_kh')
        return super(KhachHang, self).create(vals)

    def _generate_code(self, prefix, field_name):
        """Tạo mã theo prefix + số thứ tự tự động tăng"""
        # Tìm số lớn nhất hiện có
        records = self.search([(field_name, '=like', prefix + '%')])
        max_num = 0
        for rec in records:
            num_part = rec[field_name][len(prefix):]
            if num_part.isdigit():
                max_num = max(max_num, int(num_part))
        return f"{prefix}{(max_num + 1):05d}"
