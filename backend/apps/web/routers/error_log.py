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
    

# 同步用户DGC余额
wallet_locks_dict = {}
@router.get("/batch/wallet/dgc")
async def batch_wallet():
    global wallet_locks_dict
    # 若用户对应的锁不存在，则创建并添加到字典
    wallet_lock =  "system-async-wallet"
    if wallet_lock not in wallet_locks_dict:
        wallet_locks_dict[wallet_lock] = threading.Lock()
    wallet_lock = wallet_locks_dict[wallet_lock]
    wallet_lock.acquire()
    try:
        repeatFlag = True
        while repeatFlag:
            wallets = WalletTableInstance.get_wallet_dgc_page(100)
            if wallets is not None and len(wallets) > 0:
                results = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    # 使用 executor.map 执行任务
                    for result in executor.map(send_wallet_dgc, range(len(wallets)), wallets):
                        results.append(result)
                while len(results) != len(wallets):
                    print("===================多线程执行中===================", len(results))
                print("====================多线程已执行结束===================", results)
            else:
                repeatFlag = False
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 释放锁，以便该用户其他线程能获取锁并执行方法
        print("====================wallet_lock.release==================")
        wallet_lock.release()

# 同步用户DBC余额
wallet_locks_dict = {}
@router.get("/batch/wallet/dbc")
async def batch_wallet():
    global wallet_locks_dict
    # 若用户对应的锁不存在，则创建并添加到字典
    wallet_lock =  "system-async-wallet"
    if wallet_lock not in wallet_locks_dict:
        wallet_locks_dict[wallet_lock] = threading.Lock()
    wallet_lock = wallet_locks_dict[wallet_lock]
    wallet_lock.acquire()
    try:
        repeatFlag = True
        while repeatFlag:
            wallets = WalletTableInstance.get_wallet_dbc_page(100)
            if wallets is not None and len(wallets) > 0:
                results = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    # 使用 executor.map 执行任务
                    for result in executor.map(send_wallet_dbc, range(len(wallets)), wallets):
                        results.append(result)
                while len(results) != len(wallets):
                    print("===================多线程执行中===================", len(results))
                print("====================多线程已执行结束===================", results)
            else:
                repeatFlag = False
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 释放锁，以便该用户其他线程能获取锁并执行方法
        print("====================wallet_lock.release==================")
        wallet_lock.release()

def send_wallet_dgc(index: int, wallet: WalletModel):
    if wallet is not None:
        if wallet.dgc_hash is None:
            result = RewardsTableInstance.send_dgc_reward(index, wallet.user_id, wallet.dgc_amount)
            if result['hash'] is not None:
                WalletTableInstance.update_wallet_dgc(wallet.user_id, result['hash'], result['status'])
        else:
            if RewardsTableInstance.check_reward(wallet.dgc_hash):
                WalletTableInstance.update_wallet_dgc(wallet.user_id, wallet.dgc_hash, True)
    return wallet.user_id

def send_wallet_dbc(index: int, wallet: WalletModel):
    if wallet is not None:
        if wallet.dbc_hash is None:
            result = RewardsTableInstance.send_dbc_reward(index, wallet.user_id, wallet.dbc_amount)
            if result['hash'] is not None:
                WalletTableInstance.update_wallet_dbc(wallet.user_id, result['hash'], result['status'])
        else:
            if RewardsTableInstance.check_reward(wallet.dbc_hash):
                WalletTableInstance.update_wallet_dbc(wallet.user_id, wallet.dbc_hash, True)
    return wallet.user_id
