from odoo import models, fields, api
from datetime import date

from odoo.exceptions import ValidationError

class NhanVien(models.Model):
    # _name = 'nhan_vien'
    _description = 'Nhân viên'
    _rec_name = 'ma_dinh_danh'
    _order = 'name asc, tuoi desc'
    _inherit = 'hr.employee'
    
    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    que_quan = fields.Char("Quê quán")
    work_email = fields.Char(required=True)#
    mobile_phone = fields.Char(required=True)
    tuoi = fields.Integer("Tuổi", compute="_compute_tuoi", store=True)
    ngay_vao_lam = fields.Date(string='Ngày vào làm')
    trang_thai = fields.Selection(
        [('dang_lam', 'Đang làm'),
         ('tam_nghi', 'Tạm nghỉ'),
         ('thoi_viec', 'Thôi việc')],
        string="Trạng thái", default='dang_lam'
    )

    @api.constrains('ma_dinh_danh')
    def _check_ma_dinh_danh(self):
        for rec in self:
            if self.search_count([
                ('ma_dinh_danh', '=', rec.ma_dinh_danh),
                ('id', '!=', rec.id)
            ]) > 0:
                raise ValidationError("Mã nhân viên đã tồn tại!")
            
    @api.constrains('mobile_phone')
    def _check_so_dien_thoai(self):
        for rec in self:
            if self.search_count([
                ('mobile_phone', '=', rec.mobile_phone),
                ('id', '!=', rec.id)
            ]) > 0:
                raise ValidationError("Số điện thoại đã tồn tại!")
            
    @api.constrains('work_email')
    def _check_so_dien_thoai(self):
        for rec in self:
            if self.search_count([
                ('work_email', '=', rec.work_email),
                ('id', '!=', rec.id)
            ]) > 0:
                raise ValidationError("Địa chỉ email đã tồn tại!")

    @api.depends("birthday")
    def _compute_tuoi(self):
        for record in self:
            if record.birthday:
                today = date.today()
                age = today.year - record.birthday.year
                if (today.month, today.day) < (record.birthday.month, record.birthday.day):
                    raise ValidationError("Ngày sinh không hợp lệ")
                record.tuoi = age
            else:
                record.tuoi = 0
