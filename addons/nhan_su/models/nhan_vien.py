from odoo import models, fields, api
from datetime import date

from odoo.exceptions import ValidationError

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Nhân viên'
    _rec_name = 'ma_dinh_danh'
    _order = 'ten asc, tuoi desc'

    user_id = fields.Many2one('res.users', string='Tài khoản', ondelete='set null')
    
    ma_dinh_danh = fields.Char("Mã định danh", required=True)

    ho_ten_dem = fields.Char("Họ tên đệm", required=True)
    ten = fields.Char("Tên", required=True)
    ho_va_ten = fields.Char("Họ và tên", compute="_compute_ho_va_ten", store=True)
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
    ], default='nam')
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char(string='Địa chỉ email', index=True)
    so_dien_thoai = fields.Char("Số điện thoại", index=True, required=True)
    tuoi = fields.Integer("Tuổi", compute="_compute_tuoi", store=True)
    anh = fields.Binary("Ảnh")

    ngay_vao_lam = fields.Date(string='Ngày vào làm')
    don_vi_id = fields.Many2one('don_vi', string="Đơn vị")
    chuc_vu_id = fields.Many2one('chuc_vu', string="Chức vụ")
    trang_thai = fields.Selection(
        [('dang_lam', 'Đang làm'),
         ('tam_nghi', 'Tạm nghỉ'),
         ('thoi_viec', 'Thôi việc')],
        string="Trạng thái", default='dang_lam'
    )
    ghi_chu = fields.Text(string='Ghi chú')

    _sql_constraints = [
        ('ma_dinh_danh_unique', 'unique(ma_dinh_danh)', 'Mã nhân viên đã tồn tại!'),
        ('so_dien_thoai_unique', 'unique(so_dien_thoai)', 'Số điện thoại đã tồn tại!')
    ]

    @api.constrains('ma_dinh_danh')
    def _check_ma_dinh_danh(self):
        for rec in self:
            if self.search_count([
                ('ma_dinh_danh', '=', rec.ma_dinh_danh),
                ('id', '!=', rec.id)
            ]) > 0:
                raise ValidationError("Mã nhân viên đã tồn tại!")
            
    @api.constrains('so_dien_thoai')
    def _check_so_dien_thoai(self):
        for rec in self:
            if self.search_count([
                ('so_dien_thoai', '=', rec.so_dien_thoai),
                ('id', '!=', rec.id)
            ]) > 0:
                raise ValidationError("Số điện thoại đã tồn tại!")

    @api.depends("ho_ten_dem", "ten")
    def _compute_ho_va_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ho_va_ten = record.ho_ten_dem + ' ' + record.ten
                
    # @api.onchange("ten", "ho_ten_dem")
    # def _default_ma_dinh_danh(self):
    #     for record in self:
    #         if record.ho_ten_dem and record.ten:
    #             chu_cai_dau = ''.join([tu[0][0] for tu in record.ho_ten_dem.lower().split()])
    #             record.ma_dinh_danh = record.ten.lower() + chu_cai_dau
    
    @api.depends("ngay_sinh")
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                year_now = date.today().year
                record.tuoi = year_now - record.ngay_sinh.year

    @api.constrains('tuoi')
    def _check_tuoi(self):
        for record in self:
            if record.tuoi < 18:
                raise ValidationError("Tuổi không được bé hơn 18")
