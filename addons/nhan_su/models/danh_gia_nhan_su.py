from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class DanhGiaNhanSu(models.Model):
    _name = 'danh_gia_nhan_su'
    _description = 'Đánh giá nhân sự'
    _rec_name = 'display_name'
    _order = 'ngay_danh_gia desc, id desc'

    display_name = fields.Char(string='Tên hiển thị', compute='_compute_display_name', store=True)

    nhan_vien_id = fields.Many2one('hr.employee', string='Nhân viên', required=True)
    nguoi_danh_gia_id = fields.Many2one('hr.employee', string='Người đánh giá', required=True, default=lambda self: self.env.user.employee_id)
    ngay_danh_gia = fields.Date(string='Ngày đánh giá', default=fields.Date.today, required=True)
    diem = fields.Selection([
        ('0', '0 sao'),
        ('1', '1 sao'),
        ('2', '2 sao'),
        ('3', '3 sao'),
        ('4', '4 sao'),
        ('5', '5 sao'),
    ], string='Điểm đánh giá', required=True, default='5')
    nhan_xet = fields.Text(string='Nhận xét')
    trang_thai = fields.Selection([
        ('du_kien', 'Dự kiến'),
        ('da_danh_gia', 'Đã đánh giá'),
        ('huy', 'Hủy'),
    ], string='Trạng thái', default='du_kien')

    _sql_constraints = [
        ('check_diem_range', 'CHECK(diem in (\'1\',\'2\',\'3\',\'4\',\'5\'))', 'Điểm đánh giá không hợp lệ!')
    ]

    @api.depends('nhan_vien_id', 'ngay_danh_gia')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.nhan_vien_id.name} - {rec.ngay_danh_gia}"

    @api.constrains('nguoi_danh_gia_id')
    def _check_nguoi_danh_gia(self):
        for rec in self:
            if rec.nguoi_danh_gia_id == rec.nhan_vien_id:
                raise ValidationError("Người đánh giá không thể là chính nhân viên được đánh giá!")