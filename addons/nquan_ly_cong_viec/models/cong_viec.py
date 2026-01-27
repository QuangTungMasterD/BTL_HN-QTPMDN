from odoo import models, fields

class CongViec(models.Model):
    _name = "cong_viec"
    _description = "Quản lý công việc"
    _rec_name = "ten_cv"

    ma_cv = fields.Char(string="Mã công việc", required=True)
    ten_cv = fields.Char(string="Tên công việc", required=True)
    mo_ta = fields.Text(string="Mô tả công việc")
    noi_thuc_hien = fields.Char(string="Nơi thực hiện công việc", required=True)
    ngay_bd = fields.Date(string="Ngày bắt đầu làm", string=True)
    ngay_kt = fields.Date(string="Ngày hạn kết thúc", required = True)
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_lam', 'Đang làm'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy'),
    ], string='Trạng thái', default='moi')
    
