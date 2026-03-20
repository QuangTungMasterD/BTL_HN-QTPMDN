from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DuAn(models.Model):
    _inherit = 'du_an'

    cong_viec_ids = fields.One2many('cong_viec', 'du_an_id', string='Công việc')

    tong_so_cong_viec = fields.Integer(
        string='Tổng số công việc',
        compute='_tinh_tien_do_du_an',
        store=True
    )
    so_cong_viec_hoan_thanh = fields.Integer(
        string='Số công việc hoàn thành',
        compute='_tinh_tien_do_du_an',
        store=True
    )
    tien_do_phan_tram = fields.Float(
        string='Tiến độ (%)',
        compute='_tinh_tien_do_du_an',
        store=True,
        digits=(3,2)
    )

    @api.depends('cong_viec_ids', 'cong_viec_ids.trang_thai')
    def _tinh_tien_do_du_an(self):
        for du_an in self:
            # Lấy danh sách công việc từ One2many
            cong_viecs = du_an.cong_viec_ids
            tong = len(cong_viecs)
            hoan_thanh = len(cong_viecs.filtered(lambda cv: cv.trang_thai == 'hoan_thanh'))
            du_an.tong_so_cong_viec = tong
            du_an.so_cong_viec_hoan_thanh = hoan_thanh
            du_an.tien_do_phan_tram = (hoan_thanh / tong * 100) if tong > 0 else 0.0

    @api.constrains('trang_thai', 'tien_do_phan_tram')
    def _check_hoan_thanh_tien_do(self):
        for record in self:
            if record.trang_thai == 'hoan_thanh' and record.tien_do_phan_tram != 100.0:
                raise ValidationError("Không thể đánh dấu dự án hoàn thành khi tiến độ chưa đạt 100%!")
            