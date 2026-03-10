from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo import api

class CongViec(models.Model):
    _name = "cong_viec"
    _description = "Quản lý công việc"
    _rec_name = "ten_cv"

    ma_cv = fields.Char(string="Mã công việc", required=True)
    ten_cv = fields.Char(string="Tên công việc", required=True)
    mo_ta = fields.Text(string="Mô tả công việc")
    ngay_bd = fields.Date(
        string="Ngày bắt đầu làm", 
        required=True
    )
    ngay_kt = fields.Date(
        string="Ngày hạn kết thúc", 
        required = True
    )

    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_lam', 'Đang làm'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy'),
    ], string='Trạng thái', default='moi')

    bao_cao_ids = fields.One2many(
        'bao_cao_tien_do_cong_viec',
        'cong_viec_id',
        string='Báo cáo tiến độ'
    )

    nhan_vien_phu_trach_ids = fields.Many2many(
        'nhan_vien',
        string="Nhân viên phụ trách"
    )
    du_an_id = fields.Many2one(
        'du_an',
        string='Dự án',
        required=True,
        ondelete='cascade'
    )

    tien_do_hien_tai = fields.Float(
        string="Tiến độ hiện tại (%)",
        compute="_compute_tien_do_hien_tai",
        store=True,
        digits=(3,2),
        help="Tiến độ được lấy từ báo cáo mới nhất"
    )

    @api.depends('bao_cao_ids', 'bao_cao_ids.tien_do')
    def _compute_tien_do_hien_tai(self):
        for record in self:
            bao_cao_moi_nhat = record.bao_cao_ids.sorted(key=lambda r: (r.ngay_bao_cao, r.id), reverse=True)[:1]
            if bao_cao_moi_nhat:
                record.tien_do_hien_tai = bao_cao_moi_nhat.tien_do
            else:
                record.tien_do_hien_tai = 0.0

    @api.constrains('ma_cv')
    def _check_ma_cv(self):
        for rec in self:
            if self.search_count([
                ('ma_cv', '=', rec.ma_cv),
                ('id', '!=', rec.id)
            ]) > 0:
                raise ValidationError("Mã công việc đã tồn tại!")

    @api.constrains('ngay_bd', 'ngay_kt')
    def _check_ngay(self):
        for rec in self:
            if rec.ngay_bd and rec.ngay_kt and rec.ngay_kt < rec.ngay_bd:
                raise ValidationError("Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu")
    
