from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo import api

class DuAn(models.Model):
    _name = 'du_an'
    _description = 'Dự án'

    name = fields.Char(string='Tên dự án', required=True)
    mo_ta = fields.Text(string='Mô tả')
    ngay_bd = fields.Date(string='Ngày bắt đầu')
    ngay_kt = fields.Date(string='Ngày kết thúc')

    cong_viec_ids = fields.One2many(
        'cong_viec',
        'du_an_id',
        string='Công việc'
    )

    kinh_phi_ids = fields.One2many(
        'kinh_phi_du_kien',
        'du_an_id',
        string='Kinh phí dự kiến'
    )

    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('hoan_thanh', 'Hoàn thành')
    ], default='moi', string='Trạng thái')
    
    khach_hang_id = fields.Many2one(
        'khach_hang',
        string="Khách hàng",
    )

    phu_trach_id = fields.Many2one('nhan_vien', string="Nhân viên phụ trách")
    do_uu_tien = fields.Selection(
        [('thap', 'Thấp'), ('trung_binh', 'Trung bình'), ('cao', 'Cao')],
        string="Độ ưu tiên", default='trung_binh'
    )

    nhan_vien_tham_gia_ids = fields.One2many(
        'nhan_vien_tham_gia',
        'du_an_id',
        string='Nhân viên tham gia'
    )

    @api.constrains('ngay_bd', 'ngay_kt')
    def _check_ngay(self):
        for rec in self:
            if rec.ngay_bd and rec.ngay_kt and rec.ngay_kt < rec.ngay_bd:
                raise ValidationError("Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu")
    
    
