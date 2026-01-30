from odoo import models, fields

class BaoCaoTienDo(models.Model):
    _name = 'bao_cao_tien_do'
    _description = 'Báo cáo tiến độ'

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
        string='Tiến độ (%)'
    )

    noi_dung = fields.Text(string='Nội dung báo cáo')
