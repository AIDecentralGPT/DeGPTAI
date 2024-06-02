import { ApiPromise, WsProvider, Keyring } from '@polkadot/api';
import { cryptoWaitReady, blake2AsHex, randomAsU8a, mnemonicGenerate, mnemonicToMiniSecret } from '@polkadot/util-crypto';
import { formatBalance, BN_TEN, isHex, stringToU8a, u8aToHex, hexToU8a, stringToHex, hexToString } from '@polkadot/util';
import BN from 'bn.js';
import FileSaver from 'file-saver';
import { DefaultCurrentWalletData } from '$lib/constants';
import {
  showSettings,
  showNewWalletModal,
  showOpenWalletModal,
  currentWalletData,
  
} from "$lib/stores";

const node = {
  dbc: 'wss://info1.dbcwallet.io', // 公链正式链
  dbctest: 'wss://infotest.dbcwallet.io:7780'
};
let api = null;
const keyring = new Keyring({ type: 'sr25519' });

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

// 初始化与区块链节点的连接
/**
 * 初始化与区块链节点的连接
 * 获取Polkadot API实例
 */
export const GetApi = async () => {
  if (!api) {
    const provider = new WsProvider(node.dbctest);
    api = await ApiPromise.create({ provider });
  }
  return { api };
};

// 账户增删改查相关

// 创建账户
/**
 * 使用随机种子创建账户
 */
export const createAccountFromSeed = async () => {
  if (keyring) {
    await cryptoWaitReady();
    const seed = u8aToHex(randomAsU8a());
    const pair = keyring.addFromUri(seed);
    return {
      seed, // 密钥
      pair  // 账户对
    };
  }
  return null;
};

/**
 * 生成助记词并创建账户
 * @returns {object} 返回助记词和账户对
 */
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

// 导入账户
/**
 * 通过种子导入账户
 * @param {string} seed - 秘钥
 */
export const importAccountFromSeed = async (seed) => {
  await cryptoWaitReady();
  return keyring.addFromUri(seed);
};

/**
 * 通过JSON文件导入账户
 * @param {File} file - JSON文件
 */
export const importAccountFromKeystore = (file) => {
  const pairs = keyring.getPairs();
  if (pairs.length > 0) {
    keyring.removePair(pairs[0].address);
  }
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.readAsText(file);
    reader.onload = (e) => {
      const fileText = e.target?.result;
      if (fileText) {
        const json = JSON.parse(String(fileText));
        const pair = keyring.addFromJson(json);
        resolve(pair);
      }
    };
  });
};

/**
 * 从JSON导入账户
 * @param {object} json - JSON对象
 * @returns {object}
 */
export const importAccountFromJson = (json) => {
  if (keyring) {
    return keyring.addFromJson(json);
  }
  return null;
};

/**
 * 从本地存储恢复账户
 * @returns {object}
 */
export const initFromLocalstorage = () => {
  const jsonStr = localStorage.getItem('pair');
  if (keyring && jsonStr) {
    const json = JSON.parse(jsonStr);
    return importAccountFromJson(json);
  }
  return null;
};



// 导出账户

/**
 * 将账户导出为JSON文件
 * @param {object} pair - 账户对
 * @param {string} password - 密码
 */
export const exportAccountForKeystore = (pair, password) => {
  let jsonStr = localStorage.getItem('pair');
  if (!jsonStr) {
    jsonStr = JSON.stringify(pair.toJson(password));
  }
  const blob = new Blob([jsonStr], { type: 'application/json; charset=utf-8' });
  FileSaver.saveAs(blob, `${pair.address}.json`);
};





// 账户信息

/**
 * 保存账户信息到本地
 * @param {object} pair - 账户对
 * @param {string} password - 密码
 */
export const savePair = (pair, password) => {
  const jsonString = JSON.stringify(pair.toJson(password));
  console.log("jsonString", jsonString);
  localStorage.setItem('pair', jsonString);
};

/**
 * 获取所有账户对
 * @returns {Array}
 */
export const getPairs = () => {
  return keyring.getPairs() || [];
};

/**
 * 根据地址获取账户对
 * @param {string} address - 账户地址
 * @returns {object}
 */
export const getPair = (address) => {
  return keyring.getPair(address);
};

/**
 * 获取当前账户对
 * @returns {object}
 */
export const getCurrentPair = () => {
  const pairs = keyring.getPairs();
  if (pairs.length > 0) {
    return pairs[0];
  } else {
    return initFromLocalstorage();
  }
};

/**
 * 移除账户对
 * @param {string} address - 账户地址
 */
export const removePair = (address) => {
  keyring.removePair(address);
  localStorage.removeItem('pair');
};

// 余额相关

// 余额查询
/**
 * 获取当前账户的余额
 * @param {string} address - 账户地址
 * @returns {object} 返回余额信息
 */
export const onGetBalance = async (address) => {
  await GetApi();
  const balance = await api.query.system.account(address);
  let returnData = balance.toJSON();
  let reserved = getFloat(returnData.data.reserved); // 保留
  let feeFrozen = getFloat(returnData.data.feeFrozen); // 冻结
  let transfer = getFloat(Number(returnData.data.free) - Number(returnData.data.feeFrozen)); // 可转账
  let count = getFloat(Number(returnData.data.free) + Number(returnData.data.reserved)); // 全部
  return {
    transfer,
    reserved,
    feeFrozen,
    count
  };
};

/**
 * 获取当前账户的DLC余额
 * @param {string} address - 账户地址
 * @returns {object} 返回DLC余额信息
 */
export const onGetDLCBalance = async (address) => {
  await GetApi();
  const DLCBalance = await api.query.assets.account(88, address); // 可转账
  const DLCBalanceLock = await api.query.assets.assetLocks(88, address); // 锁定详情
  const DLCBalanceTotalLock = await api.query.assets.locked(88, address); // 总锁定
  const DLCBalanceData = DLCBalance.toJSON();
  const DLCBalanceLockData = DLCBalanceLock.toJSON();
  const DLCBalanceTotalLockData = DLCBalanceTotalLock.toJSON();
  const total_dlc = (DLCBalanceData ? Number(DLCBalanceData.balance) : 0) + DLCBalanceTotalLockData;
  let lockArr = [];
  if (DLCBalanceLockData) {
    for (let item in DLCBalanceLockData) {
      let data = DLCBalanceLockData[item];
      data.balance = data.balance ? (data.balance / Math.pow(10, 8)).toFixed(4) : 0;
      data.lockIndex = item;
      lockArr.push(data);
    }
  }
  return {
    balance: DLCBalanceData ? (DLCBalanceData.balance / Math.pow(10, 8)).toFixed(4) : 0,
    total_balance: total_dlc ? (total_dlc / Math.pow(10, 8)).toFixed(4) : 0,
    lockedList: lockArr
  };
};

// 查询账户余额
/**
 * 获取账户DLC和DBC余额
 * @param {string} wallet - 钱包地址
 * @returns {object} 返回余额信息
 */
export const getBalanceInfo = async (wallet) => {
  await GetApi();
  const balance = await api.query.system.account(wallet);
  const returnData = balance.toJSON();
  const transfer = getFloat(Number(returnData.data.free) - Number(returnData.data.feeFrozen)); // 可转账DBC
  const DLCBalance = await api.query.assets.account(88, wallet); // 可转账DLC
  const DLCBalanceData = DLCBalance.toJSON();
  return {
    dlc_balance: DLCBalanceData ? Number((DLCBalanceData.balance / Math.pow(10, 8)).toFixed(4)) : 0,
    dbc_balance: Number(transfer)
  };
};


// 转账
/**
 * 转账到DBC账户
 * @param {string} address - 目标DBC账户地址
 * @param {number} num - 转账金额
 * @param {string} password - 账户密码
 * @param {function} callback - 回调函数
 */
export const transferDBC = async (address, num, password, callback) => {
  await GetApi();
  const siPower = new BN(15);
  const bob = inputToBn(String(num), siPower, 15);
  let kering = getCurrentPair();
  try {
    kering.unlock(password);
  } catch (e) {
    CallBack_data1 = {
      msg: e.message,
      success: false
    };
    callback(CallBack_data1);
    return;
  }
  await cryptoWaitReady();
  await api.tx.balances
    .transfer(address, bob)
    .signAndSend(kering, ({ events = [], status }) => {
      returnFun(status, events, callback);
    })
    .catch((res) => {
      CallBack_data1 = {
        msg: res.message,
        success: false
      };
      callback(CallBack_data1);
    });
};

/**
 * 转账DLC
 * @param {string} address - 目标DLC账户地址
 * @param {number} num - 转账金额
 * @param {string} password - 账户密码
 * @param {function} callback - 回调函数
 */
export const transferDLC = async (address, num, password, callback) => {
  await GetApi();
  let kering = getCurrentPair();
  const bob = Number(num) * Math.pow(10, 8);
  try {
    kering.unlock(password);
  } catch (e) {
    CallBack_data1 = {
      msg: e.message,
      success: false
    };
    callback(CallBack_data1);
    return;
  }
  await cryptoWaitReady();
  await api.tx.assets
    .transfer(88, address, bob)
    .signAndSend(kering, ({ events = [], status }) => {
      returnFun(status, events, callback);
    })
    .catch((res) => {
      CallBack_data1 = {
        msg: res.message,
        success: false
      };
      callback(CallBack_data1);
    });
};


// 获取当前块高
/**
 * 获取当前块高
 * @returns {number} 返回块高
 */
export const onGetBlockNumber = async () => {
  await GetApi();
  const BlockNumber = await api.query.system.number();
  return BlockNumber.toJSON();
};

// 查看实时价格
/**
 * 获取链上DBC的实时价格
 * @returns {object} 返回链上DBC的实时价格
 */
export const dbcPriceOcw = async () => {
  await GetApi();
  console.log("api.query", api.query);
  
  let de = await api.query.dbcPriceOCW.avgPrice();
  console.log("de", de);
  return de.toJSON();
};




// 转账相关


// 回调函数

/**
 * 定义回调函数
 * @param {object} status - 状态
 * @param {Array} events - 事件
 * @param {function} callback - 回调函数
 */
const returnFun = (status, events, callback) => {
  if (status.isInBlock) {
    events.forEach(({ event: { method, data: [error] } }) => {
      if (method == 'ExtrinsicFailed') {
        let returnError = error;
        const decoded = api.registry.findMetaError(returnError.asModule);
        CallBack_data.msg = decoded.method;
        CallBack_data.success = false;
        CallBack_data.index = decoded.index;
        CallBack_data.section = decoded.section;
      } else if (method == 'ExtrinsicSuccess') {
        CallBack_data.msg = method;
        CallBack_data.success = true;
      }
    });
    if (callback) {
      callback(CallBack_data);
    }
  }
};

/**
 * 转换数字为浮点数
 * @param {number} number - 数字
 * @returns {string} 返回浮点数
 */
const getFloat = (number) => {
  number = number / Math.pow(10, 15);
  number = Math.round(number * 10000) / 10000;
  number = Number(number).toFixed(4);
  return number;
};





// 登录相关

/**
 * 解锁DLC
 * @param {string} password - 解锁密码
 * @param {number} lockIndex - 锁定索引
 * @param {function} callback - 回调函数
 */
export const unlockDLC = async (password, lockIndex, callback) => {
  await GetApi();
  let kering = getCurrentPair();
  try {
    kering.unlock(password);
    console.log("已解锁");
  } catch (e) {
     CallBack_data1 = {
      msg: e.message,
      success: false
    };
    callback(CallBack_data1);
    return;
  }
  await cryptoWaitReady();
  // await api.tx.assets
  //   .unlock(88, lockIndex)
  //   .signAndSend(kering, ({ events = [], status }) => {
  //     returnFun(status, events, callback);
  //   })
  //   .catch((res) => {
  //      CallBack_data1 = {
  //       msg: res.message,
  //       success: false
  //     };
  //     callback(CallBack_data1);
  //   });
};




// 工具函数

/**
 * 检查是否为Hex格式的秘钥
 * @param {string} seed - 秘钥
 * @returns {boolean}
 */
export function isHexSeed(seed) {
  return isHex(seed) && seed.length === 66;
}

/**
 * 转换输入为BN
 * @param {string} input - 输入
 * @param {BN} siPower - 精度
 * @param {BN} basePower - 基础精度
 * @returns {BN}
 */
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

  return result;
};


// 创建签名
/**
 * 创建签名
 * @param {string} nonce - 随机数
 * @param {string} data - 数据
 * @param {string} password - 密码
 * @param {string} type - 类型
 * @returns {object}
 */
export const CreateSignature = async (nonce, data, password, type) => {
  let signUrl;
  await cryptoWaitReady();
  if (type == 'seed') {
    signUrl = keyring.addFromUri(data);
  } else {
    let jsonStr = JSON.parse(JSON.stringify(data.toJson(password)));
    signUrl = keyring.addFromJson(jsonStr);
    signUrl.unlock(password);
  }
  const signature = signUrl.sign(nonce);
  return { nonce, signature: u8aToHex(signature) };
};





