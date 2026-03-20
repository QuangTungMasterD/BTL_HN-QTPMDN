from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo import api

class DuAn(models.Model):
    _name = 'du_an'
    _description = 'Dự án'
    
    _rec_name = 'display_name'
    display_name = fields.Char(string="Tên hiển thị", compute='_compute_display_name', store=True)

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

    phu_trach_id = fields.Many2one('hr.employee', string="Nhân viên phụ trách")
    do_uu_tien = fields.Selection(
        [('thap', 'Thấp'), ('trung_binh', 'Trung bình'), ('cao', 'Cao')],
        string="Độ ưu tiên", default='trung_binh'
    )

    nhan_vien_tham_gia_ids = fields.One2many(
        'nhan_vien_tham_gia',
        'du_an_id',
        string='Nhân viên tham gia'
    )

    _sql_constraints = [
        ('ma_du_an_unique', 'unique(ma_du_an)', 'Mã dự án đã tồn tại!')
    ]

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
    
    @api.constrains('phu_trach_id')
    def _check_phu_trach_chuc_vu(self):
        for record in self:
            if record.phu_trach_id:
                # Lấy tên job của nhân viên phụ trách
                job_name = record.phu_trach_id.job_id.name
                if job_name not in ('Giám đốc', 'Trưởng phòng'):
                    raise ValidationError("Nhân viên phụ trách phải có chức vụ Giám đốc hoặc Trưởng phòng!")
                if record.phu_trach_id.trang_thai != 'dang_lam':
                    raise ValidationError("Nhân viên phụ trách phải đang trong trạng thái 'Đang làm'!")

    @api.depends('ma_du_an', 'name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.ma_du_an} - {record.name}"
    
    @api.model
    def create(self, vals):
        if 'ma_du_an' not in vals:
            vals['ma_du_an'] = self._generate_code('DA', 'ma_du_an')
        return super(DuAn, self).create(vals)

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
