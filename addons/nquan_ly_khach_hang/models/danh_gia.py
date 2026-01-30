from odoo import models, fields

class DanhGia(models.Model):
    _name = 'danh_gia'
    _description = "Đánh giá của khách hàng"

    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True)
    du_an_id = fields.Many2one('du_an', string="Dự án")
    diem = fields.Selection(
        [('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')],
        string="Điểm đánh giá",
        required=True
    )
    nhan_xet = fields.Text(string="Nhận xét")
    ngay = fields.Date(string="Ngày đánh giá", default=fields.Date.today)