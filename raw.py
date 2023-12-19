import re

class YourClass:
    def detect_views_and_upload_info(self, context):
        patterns = [
            r"([\d,]+)\s+views\s+([A-Za-z]{3})\s+(\d{1,2}),\s+(\d{4})",
            r"([\d,.]+)\s+lượt xem\s+(\d{1,2})\s+thg\s+(\d{1,2}),\s+(\d{4})",
            r"([\d,]+)\s+views\s+Premiered\s+([A-Za-z]{3})\s+(\d{1,2}),\s+(\d{4})",
            r"([\d.]+)\s+lượt xem\s+Đã công chiếu vào\s+(\d{1,2})\s+thg\s+(\d{1,2}),\s+(\d{4})",
            r"([\d.]+)\s+lượt xem\s+Đã phát trực tiếp vào\s+(\d{1,2})\s+thg\s+(\d{1,2}),\s+(\d{4})",
            r"([\d]+)\s+views\s+Streamed live on\s+([A-Za-z]{3})\s+(\d{1,2}),\s+(\d{4})",
            r"([\d,]+)\s+views\s+Premiered"
        ]

        for pattern in patterns:
            match = re.search(pattern, context, re.UNICODE)
            if match:
                views = match.group(1).replace(",", "").replace(".", "")

                try:
                    day = match.group(2).zfill(2)
                    month = match.group(3).zfill(2)
                    year = match.group(4)
                except:
                    return views, None
                date = f"{day}/{month}/{year}"
                return views, date
        return None, None

# Tạo một đối tượng YourClass (hoặc đặt tên lớp của bạn)
your_instance = YourClass()

# Chuỗi mà bạn muốn kiểm tra
context = "2,344 views Premiered 22 hours ago #chungcumini #chaychungcumini #chaychungcu"

# Gọi hàm để lấy thông tin views và ngày
views, date = your_instance.detect_views_and_upload_info(context)

# In kết quả
print(f"Views: {views}")
print(f"Date: {date}")
