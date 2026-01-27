from odoo import models, fields

class KinhPhiDuKien(models.Model):
    _name = "kinh_phi_du_kien"
    _description = "Kinh phí dự kiến công việc"
    _rec_name = "ten_kc"
    
    ten_kc = fields.Char(string="Tên khoản chi", required=True)
    so_tien = fields.Float(string="Số tiền dự kiến", required=True)
    mo_ta = fields.Text(string="Mô tả số tiền của công việc")
