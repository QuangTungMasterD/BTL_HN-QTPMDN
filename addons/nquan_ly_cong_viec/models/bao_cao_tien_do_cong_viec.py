from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo import api

class BaoCaoTienDoCongViec(models.Model):
    _name = 'bao_cao_tien_do_cong_viec'
    _description = 'Báo cáo tiến độ công việc'

    cong_viec_id = fields.Many2one(
        'cong_viec',
        string='Công việc',
        ondelete='cascade',
        required=True
    )

    ngay_bao_cao = fields.Date(
        string='Ngày báo cáo',
        default=fields.Date.today
    )

    tien_do = fields.Integer(
        string='Tiến độ (%)',
        required=True
    )

    noi_dung = fields.Text(string='Nội dung báo cáo')

    nguoi_bao_cao_id = fields.Many2one(
        'nhan_vien',
        string='Người báo cáo',
        required=True,
        # domain="[('id', 'in', cong_viec_id.nhan_vien_phu_trach_ids)]"
    )

    @api.constrains('tien_do')
    def _check_tien_do(self):
        for record in self:
            if record.tien_do < 0 or record.tien_do > 100:
                raise ValidationError("Tiến độ phải từ 0 đến 100!")
    
    @api.constrains('nguoi_bao_cao_id', 'cong_viec_id')
    def _check_nguoi_bao_cao(self):
        for record in self:
            if record.cong_viec_id and record.nguoi_bao_cao_id:
                if record.nguoi_bao_cao_id not in record.cong_viec_id.nhan_vien_phu_trach_ids:
                    raise ValidationError("Người báo cáo phải là nhân viên phụ trách công việc này!")
