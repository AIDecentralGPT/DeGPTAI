from fastapi import APIRouter, Depends, HTTPException
from apps.web.models.errorlog import ErrorLogInstance, ErrorLogRequest
from apps.web.models.wallet import WalletTableInstance, WalletModel
from apps.web.models.rewards import RewardsTableInstance

import threading
import concurrent.futures

router = APIRouter()

# 添加IP记录
@router.post("/add")
async def add_err_log(errlog: ErrorLogRequest):
    try:
        errorlog = ErrorLogInstance.insert_errorlog(errlog.name, errlog.err)
        return errorlog
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# 同步用户余额
wallet_locks_dict = {}
@router.get("/batch/wallet")
async def batch_wallet():
    global wallet_locks_dict
    # 若用户对应的锁不存在，则创建并添加到字典
    wallet_lock =  "system-async-wallet"
    if wallet_lock not in wallet_locks_dict:
        wallet_locks_dict[wallet_lock] = threading.Lock()
    wallet_lock = wallet_locks_dict[wallet_lock]
    wallet_lock.acquire()
    try:
        repeat = 1
        repeatFlag = True
        while repeatFlag:
            repeat = repeat + 1
            wallets = WalletTableInstance.get_wallet_page(100)
            if wallets is not None:
                with concurrent.futures.ThreadPoolExecutor(max_workers = 20) as executor:
                    executor.map(send_wallet_account, wallets)
            else:
                repeatFlag = False
            if repeat == 2:
                repeatFlag = False
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 释放锁，以便该用户其他线程能获取锁并执行方法
        print("====================wallet_lock.release==================")
        wallet_lock.release()

def send_wallet_account(wallet: WalletModel):
    if wallet is not None:
        RewardsTableInstance.send_dgc_reward(None, wallet.user_id, wallet.amount)
        # RewardsTableInstance.send_dbc_reward(None, wallet.user_id, wallet.amount)
