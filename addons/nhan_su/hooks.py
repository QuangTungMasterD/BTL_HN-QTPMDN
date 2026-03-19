import logging

_logger = logging.getLogger(__name__)

def pre_init_hook(cr):
    _logger.info('Đang chạy pre-init hook cho module nhan_su...')

    # Tạo cột ma_dinh_danh nếu chưa tồn tại
    cr.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name='hr_employee' AND column_name='ma_dinh_danh'
    """)
    if not cr.fetchone():
        _logger.info('Tạo cột ma_dinh_danh...')
        cr.execute("ALTER TABLE hr_employee ADD COLUMN ma_dinh_danh VARCHAR")
        # Cập nhật giá trị cho cột mới
        cr.execute("UPDATE hr_employee SET ma_dinh_danh = 'EMP' || id WHERE ma_dinh_danh IS NULL")
        # Thêm ràng buộc NOT NULL (và UNIQUE nếu cần)
        cr.execute("ALTER TABLE hr_employee ALTER COLUMN ma_dinh_danh SET NOT NULL")
        # Thêm ràng buộc UNIQUE (nếu có trong _sql_constraints)
        cr.execute("ALTER TABLE hr_employee ADD CONSTRAINT ma_dinh_danh_unique UNIQUE (ma_dinh_danh)")
        _logger.info('Đã tạo cột ma_dinh_danh và thêm ràng buộc.')
    else:
        # Nếu cột đã tồn tại, chỉ cập nhật giá trị NULL
        cr.execute("UPDATE hr_employee SET ma_dinh_danh = 'EMP' || id WHERE ma_dinh_danh IS NULL OR ma_dinh_danh = ''")
        _logger.info('Đã cập nhật ma_dinh_danh cho %s bản ghi', cr.rowcount)

    # Xử lý mobile_phone (cột đã có)
    cr.execute("UPDATE hr_employee SET mobile_phone = '0000000000' || id WHERE mobile_phone IS NULL OR mobile_phone = ''")
    # Đảm bảo NOT NULL (nếu chưa có)
    cr.execute("ALTER TABLE hr_employee ALTER COLUMN mobile_phone SET NOT NULL")
    # Thêm UNIQUE nếu cần
    cr.execute("ALTER TABLE hr_employee ADD CONSTRAINT mobile_phone_unique UNIQUE (mobile_phone)")

    # Xử lý work_email
    cr.execute("UPDATE hr_employee SET work_email = 'emp' || id || '@example.com' WHERE work_email IS NULL OR work_email = ''")
    cr.execute("ALTER TABLE hr_employee ALTER COLUMN work_email SET NOT NULL")
    # UNIQUE cho email (nếu có)
    cr.execute("ALTER TABLE hr_employee ADD CONSTRAINT work_email_unique UNIQUE (work_email)")