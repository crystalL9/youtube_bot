import logging
from colorlog import ColoredFormatter

# Tạo logger và cấu hình logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Tạo một StreamHandler để đẩy log message đến stdout
console_handler = logging.StreamHandler()

# Sử dụng ColoredFormatter để có log màu trên màn hình
formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'white',
    },
    secondary_log_colors={},
    style='%'
)

console_handler.setFormatter(formatter)

# Thêm StreamHandler vào logger
logger.addHandler(console_handler)

# Ghi thông tin log
logger.debug('Đây là một thông tin log.')
