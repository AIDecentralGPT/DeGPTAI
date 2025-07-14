from peewee import *
from peewee_migrate import Router
from playhouse.db_url import connect
<<<<<<< HEAD
from config import SRC_LOG_LEVELS, DATA_DIR, DATABASE_URL
=======
from config import SRC_LOG_LEVELS, DATA_DIR
>>>>>>> fingerprintAuth-out
import os
import logging
import functools


log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["DB"])

# Check if the file exists
if os.path.exists(f"{DATA_DIR}/ollama.db"):
    # Rename the file
    os.rename(f"{DATA_DIR}/ollama.db", f"{DATA_DIR}/webui.db")
    log.info("Database migrated from Ollama-WebUI successfully.")
else:
    pass

<<<<<<< HEAD

=======
# from dotenv import load_dotenv
# load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
>>>>>>> fingerprintAuth-out
DB = connect(DATABASE_URL)
log.info(f"Connected to a {DB.__class__.__name__} database.")

router = Router(DB, migrate_dir="apps/web/internal/migrations", logger=log)
router.run()

DB.close()
DB.connect(reuse_if_open=True)

<<<<<<< HEAD
# Define a sectional decorator for wrapping database operation functions
=======
# 定义切面装饰器，用于包裹数据库操作函数
>>>>>>> fingerprintAuth-out
def aspect_database_operations(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not DB.is_closed():
            DB.close()
        DB.connect(reuse_if_open=True)
        try:
<<<<<<< HEAD
            # Execute decorated database operation functions
=======
            # 执行被装饰的数据库操作函数
>>>>>>> fingerprintAuth-out
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            return e
    return wrapper
