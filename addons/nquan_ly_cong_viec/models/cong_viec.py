from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo import api

class CongViec(models.Model):
    _name = "cong_viec"
    _description = "Quản lý công việc"
    _rec_name = 'display_name'

    display_name = fields.Char(string="Tên hiển thị", compute='_compute_display_name', store=True)

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
        'hr.employee',
        string="Nhân viên phụ trách",
        domain="[('id', 'in', available_nhan_vien_ids)]"
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

    available_nhan_vien_ids = fields.Many2many(
        'hr.employee',
        compute='_compute_available_nhan_vien_ids',
        string='Nhân viên có thể phụ trách'
    )

    @api.depends('du_an_id')
    def _compute_available_nhan_vien_ids(self):
        for record in self:
            if record.du_an_id:
                nhan_vien_list = record.du_an_id.nhan_vien_tham_gia_ids.mapped('nhan_vien_id')
                record.available_nhan_vien_ids = nhan_vien_list
            else:
                record.available_nhan_vien_ids = False

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

    @api.constrains('nhan_vien_phu_trach_ids', 'du_an_id')
    def _check_nhan_vien_thuoc_du_an(self):
        for record in self:
            if record.du_an_id and record.nhan_vien_phu_trach_ids:
                allowed_nhan_vien = record.du_an_id.nhan_vien_tham_gia_ids.mapped('nhan_vien_id')
                for nv in record.nhan_vien_phu_trach_ids:
                    if nv not in allowed_nhan_vien:
                        raise ValidationError(
                            f"Nhân viên {nv.name} không nằm trong danh sách nhân viên tham gia dự án {record.du_an_id.name}!"
                        )
                    
    @api.depends('ma_cv', 'ten_cv')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.ma_cv} - {record.ten_cv}"
