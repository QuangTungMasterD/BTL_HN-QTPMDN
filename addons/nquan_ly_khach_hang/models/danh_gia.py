from odoo import models, fields

class DanhGia(models.Model):
    _name = 'danh_gia'
    _description = "Đánh giá của khách hàng"

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