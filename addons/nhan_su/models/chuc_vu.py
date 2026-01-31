from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Bảng chứa thông tin chức vụ'
    _rec_name = 'ten_chuc_vu'

    ma_chuc_vu = fields.Char("Mã chức vụ", required=True)
    ten_chuc_vu = fields.Char("Tên chức vụ", required=True)

    @api.constrains('ma_chuc_vu')
    def _check_ma_chuc_vu(self):
        for rec in self:
            if self.search_count([
                ('ma_chuc_vu', '=', rec.ma_chuc_vu),
                ('id', '!=', rec.id)
            ]) > 0:
                raise ValidationError("Mã chức vụ đã tồn tại!")
