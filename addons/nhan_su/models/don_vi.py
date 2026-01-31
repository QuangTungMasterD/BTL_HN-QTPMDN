from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DonVi(models.Model):
    _name = 'don_vi'
    _description = 'Bảng chứa thông tin đơn vị'
    _rec_name = 'ten_don_vi'

    ma_don_vi = fields.Char("Mã đơn vị", required=True)
    ten_don_vi = fields.Char("Tên đơn vị", required=True)

    @api.constrains('ma_don_vi')
    def _check_ma_don_vi(self):
        for rec in self:
            if self.search_count([
                ('ma_don_vi', '=', rec.ma_don_vi),
                ('id', '!=', rec.id)
            ]) > 0:
                raise ValidationError("Mã đơn vị đã tồn tại!")
