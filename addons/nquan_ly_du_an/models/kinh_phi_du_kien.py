from odoo import models, fields, api
from odoo.exceptions import ValidationError

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

    @api.constrains('so_tien')
    def _check_so_tien(self):
        for record in self:
            if record.so_tien < 0:
                raise ValidationError("Số tiền không hợp lệ!")
