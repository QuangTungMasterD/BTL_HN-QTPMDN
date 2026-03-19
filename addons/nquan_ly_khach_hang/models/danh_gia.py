from odoo import models, fields, api

class DanhGia(models.Model):
    _name = 'danh_gia'
    _description = "Đánh giá của khách hàng"
    _rec_name = "display_name"
    display_name = fields.Char(string="Tên hiển thị", compute='_compute_display_name', store=True)

    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True)
    du_an_id = fields.Many2one('du_an', string="Dự án")
    diem = fields.Selection(
        [('1', '1 sao'),
        ('2', '2 sao'),
        ('3', '3 sao'),
        ('4', '4 sao'),
        ('5', '5 sao')],
        string="Điểm đánh giá",
        required=True,
        default='5'
    )
    nhan_xet = fields.Text(string="Nhận xét")
    ngay = fields.Date(string="Ngày đánh giá", default=fields.Date.today)

    @api.depends('khach_hang_id', 'du_an_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.khach_hang_id} - {record.du_an_id}"