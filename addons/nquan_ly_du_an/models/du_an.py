from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo import api

class DuAn(models.Model):
    _name = 'du_an'
    _description = 'Dự án'
    _rec_name = "ma_du_an"

    ma_du_an = fields.Char(string='Mã dự án', required=True)
    name = fields.Char(string='Tên dự án', required=True)
    mo_ta = fields.Text(string='Mô tả')
    ngay_bd = fields.Date(string='Ngày bắt đầu')
    ngay_kt_du_kien = fields.Date(string='Ngày kết thúc dự kiến')
    ngay_kt_thuc_te = fields.Date(string='Ngày kết thúc thực tế')
    ghi_chu = fields.Text(string='Ghi chú')

    kinh_phi_ids = fields.One2many(
        'kinh_phi_du_kien',
        'du_an_id',
        string='Kinh phí dự kiến'
    )

    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('tam_dung', 'Tạm dừng'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy'),
    ], default='moi', string='Trạng thái')
    
    khach_hang_id = fields.Many2one(
        'khach_hang',
        required=True,
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
    tong_so_cong_viec = fields.Integer(
        string='Tổng số công việc',
        compute='_tinh_tien_do',
        store=True
    )
    so_cong_viec_hoan_thanh = fields.Integer(
        string='Số công việc hoàn thành',
        compute='_tinh_tien_do',
        store=True
    )
    tien_do_phan_tram = fields.Float(
        string='Tiến độ (%)',
        compute='_tinh_tien_do',
        store=True,
        digits=(3,2)
    )

    _sql_constraints = [
        ('ma_du_an_unique', 'unique(ma_du_an)', 'Mã dự án đã tồn tại!')
    ]

    def _tinh_tien_do(self):
        for duan in self:
            try:
                cong_viecs = self.env['cong_viec'].search([('du_an_id', '=', duan.id)])
                tong = len(cong_viecs)
                hoan_thanh = len(cong_viecs.filtered(lambda cv: cv.trang_thai == 'hoan_thanh'))
                print(hoan_thanh)
            except KeyError:
                tong = 0
                hoan_thanh = 0
            duan.tong_so_cong_viec = tong
            duan.so_cong_viec_hoan_thanh = hoan_thanh
            if tong > 0:
                duan.tien_do_phan_tram = (hoan_thanh / tong) * 100
            else:
                duan.tien_do_phan_tram = 0.0

    @api.constrains('ngay_bd', 'ngay_kt_du_kien')
    def _check_ngay_du_kien(self):
        for rec in self:
            if rec.ngay_bd and rec.ngay_kt_du_kien and rec.ngay_kt_du_kien < rec.ngay_bd:
                raise ValidationError("Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu")
            
    @api.constrains('ngay_bd', 'ngay_kt_thuc_te')
    def _check_ngay_thuc_te(self):
        for rec in self:
            if rec.ngay_bd and rec.ngay_kt_thuc_te and rec.ngay_kt_thuc_te < rec.ngay_bd:
                raise ValidationError("Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu")
    
    
