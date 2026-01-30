from odoo import models, fields

class TuongTac(models.Model):
    _name = 'tuong_tac'
    _description = "Tương tác với khách hàng"

    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    ngay = fields.Datetime(string="Thời gian", default=fields.Datetime.now)
    kenh = fields.Selection(
        [('dien_thoai', 'Điện thoại'),
        ('email', 'Email'),
        ('truc_tiep', 'Trực tiếp')],
        string="Kênh",
        default='dien_thoai'
    )
    noi_dung = fields.Text(string="Nội dung")