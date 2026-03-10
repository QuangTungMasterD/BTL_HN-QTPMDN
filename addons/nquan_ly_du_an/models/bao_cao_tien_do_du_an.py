from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BaoCaoTienDoDuAn(models.Model):
    _name = 'bao_cao_tien_do_du_an'
    _description = 'Báo cáo tiến độ dự án'

    du_an_id = fields.Many2one(
        'du_an',
        string='Dự án',
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
        domain="[('id', '=', du_an_id.phu_trach_id)]",
        default=lambda self: self.env.user.nhan_vien_id
    )

    @api.constrains('nguoi_bao_cao_id', 'du_an_id')
    def _check_nguoi_bao_cao(self):
        for record in self:
            if record.du_an_id and record.nguoi_bao_cao_id:
                if record.nguoi_bao_cao_id != record.du_an_id.phu_trach_id:
                    raise ValidationError("Chỉ nhân viên phụ trách dự án mới được phép báo cáo!")

    @api.constrains('tien_do')
    def _check_tien_do(self):
        for record in self:
            if record.tien_do < 0 or record.tien_do > 100:
                raise ValidationError("Tiến độ phải từ 0 đến 100!")
