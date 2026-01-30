from odoo import models, fields

class KinhPhiDuKien(models.Model):
    _name = 'kinh_phi_du_kien'
    _description = 'Kinh phí dự kiến'

    du_an_id = fields.Many2one(
        'du_an',
        string='Dự án',
        ondelete='cascade',
        required=True
    )

    hang_muc = fields.Char(string='Hạng mục', required=True)
    so_tien = fields.Float(string='Số tiền')
    ghi_chu = fields.Text(string='Ghi chú')
