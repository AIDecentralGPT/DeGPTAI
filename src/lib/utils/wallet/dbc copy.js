// 留着做备份

import { ApiPromise, WsProvider, Keyring } from '@polkadot/api'
import { cryptoWaitReady, blake2AsHex, randomAsU8a, mnemonicGenerate,mnemonicToMiniSecret } from '@polkadot/util-crypto'
import { formatBalance, BN_TEN, isHex, stringToU8a, u8aToHex, hexToU8a, stringToHex, hexToString } from '@polkadot/util';
import BN from 'bn.js'
import FileSaver from 'file-saver'


const node = {
  dbc: 'wss://info1.dbcwallet.io', // 公链正式链
  dbctest: 'wss://infotest.dbcwallet.io:7780'
}

let api = null

// 链上交互
export const GetApi = async () =>{
  if (!api) {
    // const provider = new WsProvider(node.dbc)
    const provider = new WsProvider(node.dbctest)
    api = await ApiPromise.create({ 
      provider
    })
  }
  return { api }
}

// 创建账户
const keyring = new Keyring({type: 'sr25519'})
export const createAccountFromSeed = async () => {
  if (keyring) {
    await cryptoWaitReady()
    const seed = u8aToHex(randomAsU8a())
    const pair = keyring.addFromUri(seed)
    return {
      seed, // 密钥
      pair // 账户对
    }
  }
  return null
}


export const importAccountFromSeed = async (seed) => {
  await cryptoWaitReady()
  return keyring.addFromUri(seed)
}


// 导出JSON文件
export const exportAccountForKeystore = (pair, password) => {
  let jsonStr = localStorage.getItem('pair')
  if (!jsonStr) {
    jsonStr = JSON.stringify(pair.toJson(password))
  }
  const blob = new Blob([jsonStr], {type: 'application/json; charset=utf-8'});
  FileSaver.saveAs(blob, `${pair.address}.json`);
}

// 保存在localStore
export const savePair = (pair, password) => {
  const jsonString = JSON.stringify(pair.toJson(password))
  console.log("jsonString", jsonString);
  localStorage.setItem('pair', jsonString)
}

// 导入JSON文件
export const importAccountFromKeystore = (file) => {
  const pairs = keyring.getPairs()
  if (pairs.length > 0) {
    keyring.removePair(pairs[0].address)
  }
  return new Promise(resolve => {
    const reader = new FileReader()
    reader.readAsText(file)
    reader.onload = (e) => {
      const fileText = e.target?.result
      if (fileText) {
        const json = JSON.parse(String(fileText))
        const pair = keyring.addFromJson(json)
        resolve(pair)
      }
    }
  })
}

// 工具
export function isHexSeed(seed) {
  return isHex(seed) && seed.length === 66;
}

export const getPairs = () => {
  return keyring.getPairs() || []
}
export const getPair = (address) => {
  return keyring.getPair(address)
}
// 获取当前账户
export const getCurrentPair = () => {
  const pairs = keyring.getPairs()
  if (pairs.length > 0) {
    return pairs[0]
  } else {
    return initFromLocalstorage()
  }
}

// 从本地存储恢复账户
export const initFromLocalstorage = () => {
  const jsonStr = localStorage.getItem('pair')
  if (keyring && jsonStr) {
    const json = JSON.parse(jsonStr)
    return importAccountFromJson(json)
  }
  return null
}

export const importAccountFromJson = (json) => {
  if (keyring) {
    return keyring.addFromJson(json)
  }
  return null
}

// 移除账户
export const removePair = (address) => {
  keyring.removePair(address)
  localStorage.removeItem('pair')
}

// 生成签名
export const CreateSignature = async (nonce, data, password, type) => {
  let signUrl;
  await cryptoWaitReady();
  if (type == 'seed') {
    signUrl = keyring.addFromUri(data);
  } else {
    let jsonStr = JSON.parse(JSON.stringify(data.toJson(password)))
    signUrl = keyring.addFromJson(jsonStr);
    signUrl.unlock(password)
  }
  const signature = signUrl.sign(nonce);
  return {nonce, signature: u8aToHex(signature)}
}

/**
 * dbcPriceOcw 获取链上DBC的实时价格
 * 
 * @return data:返回链上DBC的实时价格
 */
export const dbcPriceOcw = async () => {
  await GetApi()
  let de = await api.query.dbcPriceOCW.avgPrice();
  console.log("de", de);
  return de.toJSON()
}

let CallBack_data = {
  index: 0,
  msg:'',
  section:'',
  success: false
} 
let CallBack_data1 = {
  msg:'',
  success: false
}

export const inputToBn = (input, siPower, basePower) => {
  const isDecimalValue = input.match(/^(\d+)\.(\d+)$/);

  let result;

  if (isDecimalValue) {
    const div = new BN(input.replace(/\.\d*$/, ''));
    const modString = input.replace(/^\d+\./, '').substr(0, api?.registry.chainDecimals[0]);
    const mod = new BN(modString);
    result = div
      .mul(BN_TEN.pow(siPower))
      .add(mod.mul(BN_TEN.pow(new BN(basePower - modString.length))));
  } else {
    result = new BN(input.replace(/[^\d]/g, ''))
      .mul(BN_TEN.pow(siPower));
  }

  return result
}

// 定义回调函数
const returnFun = (status, events, callback) => {
  if (status.isInBlock) {
    events.forEach(({ event: { method, data: [error] } }) => {
      if (method == 'ExtrinsicFailed') {
        let returnError = error
        const decoded = api.registry.findMetaError(returnError.asModule);
        CallBack_data.msg = decoded.method;
        CallBack_data.success = false
        CallBack_data.index = decoded.index;
        CallBack_data.section = decoded.section;
      }else if(method == 'ExtrinsicSuccess'){
        CallBack_data.msg = method;
        CallBack_data.success = true
      }
    });
    if (callback) {
      callback(CallBack_data)
    }
  }
}

const getFloat = (number) => {
  number = number/Math.pow(10, 15)
  number = Math.round(number*10000)/10000
  number = Number(number).toFixed(4)
  return number
}

// 获得当前账户的余额
export const onGetBalance = async (address) => {
  await GetApi()
  const balance = await api.query.system.account(address)
  let returnData = balance.toJSON()
  let reserved = getFloat(returnData.data.reserved) // 保留
  let feeFrozen = getFloat(returnData.data.feeFrozen) // 冻结
  let transfer = getFloat(Number(returnData.data.free) - Number(returnData.data.feeFrozen)) // 可转账
  let count = getFloat(Number(returnData.data.free) + Number(returnData.data.reserved)) // 全部
  return {
    transfer,
    reserved,
    feeFrozen,
    count
  }
}

// 获得当前账户的DLC余额
export const onGetDLCBalance = async (address) => {
  await GetApi()
  const DLCBalance = await api.query.assets.account(88, address) // 可转账
  const DLCBalanceLock = await api.query.assets.assetLocks(88, address) // 锁定详情
  const DLCBalanceTotalLock = await api.query.assets.locked(88, address) // 总锁定
  const DLCBalanceData = DLCBalance.toJSON()
  const DLCBalanceLockData = DLCBalanceLock.toJSON()
  const DLCBalanceTotalLockData = DLCBalanceTotalLock.toJSON()
  const total_dlc =  (DLCBalanceData ? Number(DLCBalanceData.balance) : 0) + DLCBalanceTotalLockData
  let lockArr = []
  if (DLCBalanceLockData) {
    for (let item in DLCBalanceLockData) {
      let data = DLCBalanceLockData[item]
      data.balance = data.balance ? (data.balance/Math.pow(10, 8)).toFixed(4) : 0
      data.lockIndex = item
      lockArr.push(data)
    }
  }
  return {
    balance: DLCBalanceData ? (DLCBalanceData.balance/Math.pow(10, 8)).toFixed(4) : 0,
    total_balance: total_dlc ? (total_dlc/Math.pow(10, 8)).toFixed(4) : 0,
    lockedList: lockArr
  }
}

// 获得当前块高
export const onGetBlockNumber = async () => {
  await GetApi()
  const BlockNumber = await api.query.system.number()
  return BlockNumber.toJSON()
}

// 解除锁定
/**
 * 解锁DLC
 *
 * @param password 解锁密码
 * @param lockIndex 锁定索引
 * @param callback 回调函数
 * @returns Promise<void>
 */
export const unlockDLC = async (password, lockIndex, callback) => {
  await GetApi()
  let kering = getCurrentPair()
  try {
    kering.unlock(password)
  } catch (e) {
    CallBack_data1 = {
      msg: e.message,
      success: false
    };
    callback(CallBack_data1)
    return;
  }
  await cryptoWaitReady();
  await api.tx.assets
  .unlock( 88, lockIndex )
  .signAndSend( kering , ( { events = [], status  } ) => {
    returnFun(status, events, callback)
  })
  .catch((res)=>{
    CallBack_data1 = {
      msg: res.message,
      success: false
    };
    callback(CallBack_data1)
  })
}


/**
 * 转账到DBC账户
 *
 * @param address 目标DBC账户地址
 * @param num 转账金额
 * @param password 账户密码
 * @param callback 回调函数
 * @returns 无返回值
 */
export const transferDBC = async (address, num, password, callback) => {
  await GetApi();
  const siPower = new BN(15)
  const bob = inputToBn(String(num), siPower, 15)
  let kering = getCurrentPair()
  try {
    kering.unlock(password)
  } catch (e) {
    CallBack_data1 = {
      msg: e.message,
      success: false
    };
    callback(CallBack_data1)
    return;
  }
  await cryptoWaitReady();
  await api.tx.balances
  .transfer( address, bob )
  .signAndSend( kering , ( { events = [], status  } ) => {
    returnFun(status, events, callback)
  })
  .catch((res)=>{
    CallBack_data1 = {
      msg: res.message,
      success: false
    };
    callback(CallBack_data1)
  })
}

export const transferDLC = async (address, num, password, callback) => {
  await GetApi();
  let kering = getCurrentPair()
  const bob = Number(num) * Math.pow(10, 8)
  try {
    kering.unlock(password)
  } catch (e) {
    CallBack_data1 = {
      msg: e.message,
      success: false
    };
    callback(CallBack_data1)
    return;
  }
  await cryptoWaitReady();
  await api.tx.assets
  .transfer( 88, address, bob )
  .signAndSend( kering , ( { events = [], status  } ) => {
    returnFun(status, events, callback)
  })
  .catch((res)=>{
    CallBack_data1 = {
      msg: res.message,
      success: false
    };
    callback(CallBack_data1)
  })
}

// 获取账户DLC-DBC余额
export const getBalanceInfo = async (wallet) => {
  await GetApi()
  const balance = await api.query.system.account(wallet)
  const returnData = balance.toJSON()
  const transfer = getFloat(Number(returnData.data.free) - Number(returnData.data.feeFrozen)) // 可转账DBC
  const DLCBalance = await api.query.assets.account(88, wallet) // 可转账DLC
  const DLCBalanceData = DLCBalance.toJSON()
  return {
    dlc_balance: DLCBalanceData ? Number((DLCBalanceData.balance/Math.pow(10, 8)).toFixed(4)) : 0,
    dbc_balance: Number(transfer)
  }
}


// 生成助记词并创建账户：
export const createAccountFromMnemonic = async () => {
  await cryptoWaitReady(); // 确保加密库已准备好
  const mnemonic = mnemonicGenerate(); // 生成助记词
  const pair = keyring.addFromUri(mnemonic); // 使用助记词创建账户对
  console.log(`Generated mnemonic: ${mnemonic}`); // 输出生成的助记词
  return {
    mnemonic, // 返回生成的助记词
    pair // 返回账户对
  };
};