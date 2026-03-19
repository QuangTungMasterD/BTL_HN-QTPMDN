from odoo import models, fields

class LichHen(models.Model):
    _name = 'lich_hen'
    _description = "Lịch hẹn với khách hàng"
    _rec_name = "khach_hang_id"

    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên phụ trách", required=True)
    thoi_gian = fields.Datetime(string="Thời gian hẹn", required=True)
    dia_diem = fields.Char(string="Địa điểm")
    noi_dung = fields.Text(string="Nội dung dự kiến")
    trang_thai = fields.Selection(
        [('du_kien', 'Dự kiến'),
        ('da_hen', 'Đã hẹn'),
        ('da_xong', 'Đã xong'),
        ('huy', 'Hủy')],
        string="Trạng thái", default='du_kien'
    )