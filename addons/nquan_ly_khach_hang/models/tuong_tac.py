from odoo import models, fields

class TuongTac(models.Model):
    _name = 'tuong_tac'
    _description = "Tương tác với khách hàng"
    _rec_name = "khach_hang_id"

    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True)
    nhan_vien_id = fields.Many2one('hr.employee', string="Nhân viên", required=True)
    ngay = fields.Datetime(string="Thời gian", default=fields.Datetime.now)
    kenh = fields.Selection([
        ('dien_thoai', 'Điện thoại'),
        ('email', 'Email'),
        ('truc_tiep', 'Trực tiếp'),
        ('khac', 'Khác')],
        string="Kênh",
        default='dien_thoai'
    )
    noi_dung = fields.Text(string="Nội dung")