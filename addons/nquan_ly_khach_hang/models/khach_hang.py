from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

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
    ten_cong_ty = fields.Char(string="Tên công ty")
    ma_so_thue = fields.Char(string="Mã số thuế")
    so_cccd = fields.Char(string="Số CCCD", required=True)
    ghi_chu = fields.Text(string="Ghi chú")

    @api.constrains('loai_kh', 'ma_so_thue', 'ten_cong_ty')
    def _check_company_fields(self):
        for record in self:
            if record.loai_kh == 'doanh_nghiep':
                if not record.ma_so_thue:
                    raise ValidationError("Vui lòng nhập mã số thuế cho khách hàng doanh nghiệp!")
                if not record.ten_cong_ty:
                    raise ValidationError("Vui lòng nhập tên công ty cho khách hàng doanh nghiệp!")

    @api.constrains('so_cccd')
    def _check_so_cccd(self):
        for rec in self:
            if rec.so_cccd and not re.match(r'^\d{12}$', rec.so_cccd):
                raise ValidationError("Số CCCD phải gồm đúng 12 chữ số!")
    
    @api.constrains('so_cccd')
    def _check_unique_cccd(self):
        for rec in self:
            if self.search_count([
                ('so_cccd', '=', rec.so_cccd),
                ('id', '!=', rec.id)
            ]) > 0:
                raise ValidationError("CCCD khách hàng đã tồn tại!")

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
