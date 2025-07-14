import { ApiPromise, WsProvider, Keyring } from "@polkadot/api";
import {
  cryptoWaitReady,
  randomAsU8a,
  mnemonicGenerate,
} from "@polkadot/util-crypto";
import {
  BN_TEN,
  isHex,
  stringToU8a,
  u8aToHex,
} from "@polkadot/util";
import BN from "bn.js";
import FileSaver from "file-saver";

import { v4 as uuidv4 } from 'uuid';

const node = {
<<<<<<< HEAD
  dbc: "wss://info1.dbcwallet.io", // Public Chain Official Chain
=======
  dbc: "wss://info1.dbcwallet.io", // 公链正式链
>>>>>>> fingerprintAuth-out
  dbctest: "wss://infotest.dbcwallet.io:7780",
};
let api = null;
const keyring = new Keyring({ type: "sr25519" });

let CallBack_data = {
  index: 0,
  msg: "",
  section: "",
  success: false,
};
let CallBack_data1 = {
  msg: "",
  success: false,
};

<<<<<<< HEAD
/**
 * Initialize the connection with blockchain nodes
 * Get Polkadot API instance
=======
// 初始化与区块链节点的连接
/**
 * 初始化与区块链节点的连接
 * 获取Polkadot API实例
>>>>>>> fingerprintAuth-out
 */
export const GetApi = async () => {
  if (!api) {
    const provider = new WsProvider(node.dbctest);
    api = await ApiPromise.create({ provider });
  }
  return { api };
};

<<<<<<< HEAD
// Account addition, deletion, modification, and query related

// Create an account
/**
 * Create an account using random seeds
=======
// 账户增删改查相关

// 创建账户
/**
 * 使用随机种子创建账户
>>>>>>> fingerprintAuth-out
 */
export const createAccountFromSeed = async () => {
  if (keyring) {
    await cryptoWaitReady();
    const seed = u8aToHex(randomAsU8a());
    const pair = keyring.addFromUri(seed);
    return {
<<<<<<< HEAD
      seed, // secret key
      pair, // account pairs
=======
      seed, // 密钥
      pair, // 账户对
>>>>>>> fingerprintAuth-out
    };
  }
  return null;
};

/**
<<<<<<< HEAD
 * Generate mnemonic words and create an account
 * @returns {object} Return mnemonic words and account pairs
 */
export const createAccountFromMnemonic = async () => {
  await cryptoWaitReady(); // Ensure that the encryption library is ready
  const mnemonic = mnemonicGenerate(); // Generate mnemonic words
  const pair = keyring.addFromUri(mnemonic); // Create an account using mnemonic words
  console.log(`Generated mnemonic: ${mnemonic}`); // Output generated mnemonic words
  return {
    mnemonic, // Return the generated mnemonic words
    pair, // Return to account
  };
};

/**
 * Import account through seed
 * @param {string} seed - secret key
=======
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
    pair, // 返回账户对
  };
};

// 导入账户
/**
 * 通过种子导入账户
 * @param {string} seed - 秘钥
>>>>>>> fingerprintAuth-out
 */
export const importAccountFromSeed = async (seed) => {
  await cryptoWaitReady();
  return keyring.addFromUri(seed);
};

/**
<<<<<<< HEAD
 * Import account through JSON file
 * @param {File} file - JSON fole
=======
 * 通过JSON文件导入账户
 * @param {File} file - JSON文件
>>>>>>> fingerprintAuth-out
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
<<<<<<< HEAD
 * Import account from JSON
 * @param {object} json - JSON object
=======
 * 从JSON导入账户
 * @param {object} json - JSON对象
>>>>>>> fingerprintAuth-out
 * @returns {object}
 */
export const importAccountFromJson = (json) => {
  if (keyring) {
    return keyring.addFromJson(json);
  }
  return null;
};

/**
<<<<<<< HEAD
 * Restore account from local storage
=======
 * 从本地存储恢复账户
>>>>>>> fingerprintAuth-out
 * @returns {object}
 */
export const initFromLocalstorage = () => {
  const jsonStr = localStorage.getItem("pair");
<<<<<<< HEAD
  console.log("Get jsonStr locally:", jsonStr);
=======
  console.log("从本地获取的jsonStr", jsonStr);
>>>>>>> fingerprintAuth-out
  
  if (keyring && jsonStr) {
    const json = JSON.parse(jsonStr);
    return importAccountFromJson(json);
  }
  return null;
};

<<<<<<< HEAD
/**
 * Export the account as a JSON file
 * @param {object} pair - account pairs
 * @param {string} password - password
=======
// 导出账户

/**
 * 将账户导出为JSON文件
 * @param {object} pair - 账户对
 * @param {string} password - 密码
>>>>>>> fingerprintAuth-out
 */
export const exportAccountForKeystore = (pair, password = "") => {
  console.log("password", password);
  console.log("pair", pair);
  
  
  let jsonStr = localStorage.getItem("pair");
  if (!jsonStr) {
    jsonStr = JSON.stringify(pair.toJson(password));
  }
  const blob = new Blob([jsonStr], { type: "application/json; charset=utf-8" });
  FileSaver.saveAs(blob, `${pair.address}.json`);
};

<<<<<<< HEAD

/**
 * Save account information locally
 * @param {object} pair - account pairs
 * @param {string} password - password
=======
// 账户信息

/**
 * 保存账户信息到本地
 * @param {object} pair - 账户对
 * @param {string} password - 密码
>>>>>>> fingerprintAuth-out
 */
export const savePair = (pair, password) => {
  const jsonString = JSON.stringify(pair.toJson(password));
  console.log("jsonString", jsonString);
  localStorage.setItem("pair", jsonString);
};

/**
<<<<<<< HEAD
 * Get all account pairs
=======
 * 获取所有账户对
>>>>>>> fingerprintAuth-out
 * @returns {Array}
 */
export const getPairs = () => {
  return keyring.getPairs() || [];
};

/**
<<<<<<< HEAD
 * Obtain account pairs based on address
 * @param {string} address - Account address
=======
 * 根据地址获取账户对
 * @param {string} address - 账户地址
>>>>>>> fingerprintAuth-out
 * @returns {object}
 */
export const getPair = (address) => {
  return keyring.getPair(address);
};

/**
<<<<<<< HEAD
 * Get the current account pair
=======
 * 获取当前账户对
>>>>>>> fingerprintAuth-out
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
<<<<<<< HEAD
 * Remove account pair
 * @param {string} address - Account address
=======
 * 移除账户对
 * @param {string} address - 账户地址
>>>>>>> fingerprintAuth-out
 */
export const removePair = (address) => {
  keyring.removePair(address);
  localStorage.removeItem("pair");
};

<<<<<<< HEAD
// Balance related
/**
 * Get the balance of the current account
 * @param {string} address - Account address
 * @returns {object} Return balance information
=======
// 余额相关

// 余额查询
/**
 * 获取当前账户的余额
 * @param {string} address - 账户地址
 * @returns {object} 返回余额信息
>>>>>>> fingerprintAuth-out
 */
export const onGetBalance = async (address) => {
  await GetApi();
  const balance = await api.query.system.account(address);
  let returnData = balance.toJSON();

<<<<<<< HEAD
  console.log("balance returnData", returnData);
  

  let reserved = getFloat(returnData.data.reserved);
  let feeFrozen = getFloat(returnData.data.feeFrozen);
  let transfer = getFloat(
    Number(returnData.data.free) - Number(returnData.data.feeFrozen)
  );
  let count = getFloat(
    Number(returnData.data.free) + Number(returnData.data.reserved)
  );
=======
  console.log("余额呀returnData", returnData);
  

  let reserved = getFloat(returnData.data.reserved); // 保留
  let feeFrozen = getFloat(returnData.data.feeFrozen); // 冻结
  let transfer = getFloat(
    Number(returnData.data.free) - Number(returnData.data.feeFrozen)
  ); // 可转账
  let count = getFloat(
    Number(returnData.data.free) + Number(returnData.data.reserved)
  ); // 全部
>>>>>>> fingerprintAuth-out
  return {
    transfer,
    reserved,
    feeFrozen,
    count,
  };
};

/**
<<<<<<< HEAD
 * Get the DLC balance of the current account
 * @param {string} address - Account address
 * @returns {object} Return DLC balance information
 */
export const onGetDLCBalance = async (address) => {
  await GetApi();
  const DLCBalance = await api.query.assets.account(88, address);
  const DLCBalanceLock = await api.query.assets.assetLocks(88, address);
  const DLCBalanceTotalLock = await api.query.assets.locked(88, address);
=======
 * 获取当前账户的DLC余额
 * @param {string} address - 账户地址
 * @returns {object} 返回DLC余额信息
 */
export const onGetDLCBalance = async (address) => {
  await GetApi();
  const DLCBalance = await api.query.assets.account(88, address); // 可转账
  const DLCBalanceLock = await api.query.assets.assetLocks(88, address); // 锁定详情
  const DLCBalanceTotalLock = await api.query.assets.locked(88, address); // 总锁定
>>>>>>> fingerprintAuth-out
  const DLCBalanceData = DLCBalance.toJSON();
  const DLCBalanceLockData = DLCBalanceLock.toJSON();
  const DLCBalanceTotalLockData = DLCBalanceTotalLock.toJSON();
  const total_dlc =
    (DLCBalanceData ? Number(DLCBalanceData.balance) : 0) +
    DLCBalanceTotalLockData;
  let lockArr = [];
  if (DLCBalanceLockData) {
    for (let item in DLCBalanceLockData) {
      let data = DLCBalanceLockData[item];
      data.balance = data.balance
        ? (data.balance / Math.pow(10, 8)).toFixed(4)
        : 0;
      data.lockIndex = item;
      lockArr.push(data);
    }
  }
  return {
    balance: DLCBalanceData
      ? (DLCBalanceData.balance / Math.pow(10, 8)).toFixed(4)
      : 0,
    total_balance: total_dlc ? (total_dlc / Math.pow(10, 8)).toFixed(4) : 0,
    lockedList: lockArr,
  };
};

<<<<<<< HEAD
// Check account balance
/**
 * Obtain account DLC and DBC balance
 * @param {string} wallet - Account address
 * @returns {object} Return balance information
=======
// 查询账户余额
/**
 * 获取账户DLC和DBC余额
 * @param {string} wallet - 钱包地址
 * @returns {object} 返回余额信息
>>>>>>> fingerprintAuth-out
 */
export const getBalanceInfo = async (wallet) => {
  await GetApi();
  const balance = await api.query.system.account(wallet);
  const returnData = balance.toJSON();
  const transfer = getFloat(
    Number(returnData.data.free) - Number(returnData.data.feeFrozen)
<<<<<<< HEAD
  );
  const DLCBalance = await api.query.assets.account(88, wallet);
=======
  ); // 可转账DBC
  const DLCBalance = await api.query.assets.account(88, wallet); // 可转账DLC
>>>>>>> fingerprintAuth-out
  const DLCBalanceData = DLCBalance.toJSON();
  return {
    dlc_balance: DLCBalanceData
      ? Number((DLCBalanceData.balance / Math.pow(10, 8)).toFixed(4))
      : 0,
    dbc_balance: Number(transfer),
  };
};

<<<<<<< HEAD
/**
 * Transfer to DBC account
 * @param {string} address - Target DBC account address
 * @param {number} num - Transfer amount
 * @param {string} password - Account password
 * @param {function} callback - callback
=======
// 转账
/**
 * 转账到DBC账户
 * @param {string} address - 目标DBC账户地址
 * @param {number} num - 转账金额
 * @param {string} password - 账户密码
 * @param {function} callback - 回调函数
>>>>>>> fingerprintAuth-out
 */
export const transferDBC = async (address, num, password, callback) => {
  await GetApi();
  const siPower = new BN(15);
  const bob = inputToBn(String(num), siPower, 15);
  let kering = getCurrentPair();
  try {
    kering?.unlock(password);
  } catch (e) {
<<<<<<< HEAD
    console.log("transferDBC fun", e);
=======
    console.log("transferDBC方法", e);
>>>>>>> fingerprintAuth-out
    
    CallBack_data1 = {
      msg: e.message,
      success: false,
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
<<<<<<< HEAD
      console.log("transferDBC fun", res);
=======
      console.log("transferDBC方法", res);
>>>>>>> fingerprintAuth-out

      CallBack_data1 = {
        msg: res.message,
        success: false,
      };
      callback(CallBack_data1);
    });
};

/**
<<<<<<< HEAD
 * Transfer DLC
 * @param {string} address - Target DLC account address
 * @param {number} num - Transfer amount
 * @param {string} password - Account password
 * @param {function} callback - callback
=======
 * 转账DLC
 * @param {string} address - 目标DLC账户地址
 * @param {number} num - 转账金额
 * @param {string} password - 账户密码
 * @param {function} callback - 回调函数
>>>>>>> fingerprintAuth-out
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
      success: false,
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
        success: false,
      };
      callback(CallBack_data1);
    });
};

<<<<<<< HEAD
// Get the current block height
/**
 * Get the current block height
 * @returns {number} Return block height
=======
// 获取当前块高
/**
 * 获取当前块高
 * @returns {number} 返回块高
>>>>>>> fingerprintAuth-out
 */
export const onGetBlockNumber = async () => {
  await GetApi();
  const BlockNumber = await api.query.system.number();
  return BlockNumber.toJSON();
};

<<<<<<< HEAD
// View real-time prices
/**
 * Get real-time prices of DBC on the chain
 * @returns {object} Return the real-time price of DBC on the chain
=======
// 查看实时价格
/**
 * 获取链上DBC的实时价格
 * @returns {object} 返回链上DBC的实时价格
>>>>>>> fingerprintAuth-out
 */
export const dbcPriceOcw = async () => {
  await GetApi();
  console.log("api.query", api.query);

  let de = await api.query.dbcPriceOCW.avgPrice();
  console.log("de", de);
  return de.toJSON();
};

<<<<<<< HEAD
// Transfer related
/**
 * Define callback function
 * @param {object} status - status
 * @param {Array} events - events
 * @param {function} callback - callback
=======
// 转账相关

// 回调函数

/**
 * 定义回调函数
 * @param {object} status - 状态
 * @param {Array} events - 事件
 * @param {function} callback - 回调函数
>>>>>>> fingerprintAuth-out
 */
const returnFun = (status, events, callback) => {
  if (status.isInBlock) {
    events.forEach(
      ({
        event: {
          method,
          data: [error],
        },
      }) => {
        if (method == "ExtrinsicFailed") {
          let returnError = error;
          const decoded = api.registry.findMetaError(returnError.asModule);
          CallBack_data.msg = decoded.method;
          CallBack_data.success = false;
          CallBack_data.index = decoded.index;
          CallBack_data.section = decoded.section;
        } else if (method == "ExtrinsicSuccess") {
          CallBack_data.msg = method;
          CallBack_data.success = true;
        }
      }
    );
    if (callback) {
      callback(CallBack_data);
    }
  }
};

/**
<<<<<<< HEAD
 * Convert numbers to floating-point numbers
 * @param {number} number - number
 * @returns {string} Return floating point number
=======
 * 转换数字为浮点数
 * @param {number} number - 数字
 * @returns {string} 返回浮点数
>>>>>>> fingerprintAuth-out
 */
const getFloat = (number) => {
  number = number / Math.pow(10, 15);
  number = Math.round(number * 10000) / 10000;
  number = Number(number).toFixed(4);
  return number;
};

<<<<<<< HEAD
// Login related
/**
 * Unlock DLC
 * @param {string} password - Unlock password
 * @param {number} lockIndex - Lock index
 * @param {function} callback - callback
 */
export const unlockDLC = async (password, lockIndex, callback) => {
  // Call the FHIR pi function
  await GetApi();
  // Get current pairing
  let kering = getCurrentPair();
  try {
    // Local password unlock
    kering.unlock(password);
    console.log("Unlocked");
=======
// 登录相关

/**
 * 解锁DLC
 * @param {string} password - 解锁密码
 * @param {number} lockIndex - 锁定索引
 * @param {function} callback - 回调函数
 */
export const unlockDLC = async (password, lockIndex, callback) => {
  // 调用 GetApi 函数
  await GetApi();
  // 获取当前配对
  let kering = getCurrentPair();
  try {
    // 本地密码解锁
    kering.unlock(password);
    console.log("已解锁");
>>>>>>> fingerprintAuth-out
    callback({
      success: true
    }) 
  } catch (e) {

<<<<<<< HEAD
    // Set error callback data
=======
    // 设置错误回调数据
>>>>>>> fingerprintAuth-out
    CallBack_data1 = {
      msg: e.message,
      success: false,
    };
<<<<<<< HEAD
    // Call callback function and pass in error callback data
    callback(CallBack_data1);
    return;
  }
};


// utilities
/**
 * Check if the key is in Hex format
 * @param {string} seed - secret key
=======
    // 调用回调函数并传入错误回调数据
    callback(CallBack_data1);
    return;
  }
  // 等待加密操作准备就绪
  // await cryptoWaitReady();

  // 联网解锁，解锁资产
  // await api.tx.assets
  //   .unlock(88, lockIndex)
  //   .signAndSend(kering, ({ events = [], status }) => {
  //     // 调用 returnFun 函数处理结果
  //     returnFun(status, events, callback);
  //   })
  //   .catch((res) => {
  //   console.log(222);
  //   // 设置错误回调数据
  //   CallBack_data1 = {
  //       msg: res.message,
  //       success: false
  //     };
  //     // 调用回调函数并传入错误回调数据
  //     callback(CallBack_data1);
  //   });
};


// 工具函数

/**
 * 检查是否为Hex格式的秘钥
 * @param {string} seed - 秘钥
>>>>>>> fingerprintAuth-out
 * @returns {boolean}
 */
export function isHexSeed(seed) {
  return isHex(seed) && seed.length === 66;
}

/**
<<<<<<< HEAD
 * Convert input to BN
 * @param {string} input - input
 * @param {BN} siPower - accuracy
 * @param {BN} basePower - basePower
=======
 * 转换输入为BN
 * @param {string} input - 输入
 * @param {BN} siPower - 精度
 * @param {BN} basePower - 基础精度
>>>>>>> fingerprintAuth-out
 * @returns {BN}
 */
export const inputToBn = (input, siPower, basePower) => {
  const isDecimalValue = input.match(/^(\d+)\.(\d+)$/);

  let result;

  if (isDecimalValue) {
    const div = new BN(input.replace(/\.\d*$/, ""));
    const modString = input
      .replace(/^\d+\./, "")
      .substr(0, api?.registry.chainDecimals[0]);
    const mod = new BN(modString);
    result = div
      .mul(BN_TEN.pow(siPower))
      .add(mod.mul(BN_TEN.pow(new BN(basePower - modString.length))));
  } else {
    result = new BN(input.replace(/[^\d]/g, "")).mul(BN_TEN.pow(siPower));
  }

  return result;
};

<<<<<<< HEAD

// Create Signature
export const signData = async (data, password, type) => {
  const nonce = uuidv4();
  // const nonce = "test";
  const nonceU8a = stringToU8a(nonce); // Convert to Uint8Array
=======
// 创建签名
// /**
//  * 创建签名
//  * @param {string} nonce - 随机数
//  * @param {string} data - 数据
//  * @param {string} password - 密码
//  * @param {string} type - 类型
//  * @returns {object}
//  * 
//  * nonce 是一个随机数，它用于确保每次签名都是唯一的，以防止重放攻击。
//   data 是你要签名的数据。这可以是任何数据，但通常是交易的一部分。
//   password 是用于解锁账户密钥的密码。这是为了确保只有知道密码的人才能签名。
//   type 参数是用来指定data参数的类型。如果type为 "seed"，那么data参数应该是一个种子，将用于通过keyring.addFromUri(data)方法创建一个新的密钥对。如果type不是 "seed"，那么data参数应该是一个账户对，它将被转换为JSON格式，并通过keyring.addFromJson(jsonStr)方法导入。

//  */
// // export const CreateSignature = async (nonce, data, password, type) => {
// export const signData = async (data, password, type) => {
//   const nonce = uuidv4()
//   // const nonce = stringToU8a(uuidv4());  // 转换为 Uint8Array

//   let signUrl;
//   await cryptoWaitReady();
//   if (type == "seed") {
//     signUrl = keyring.addFromUri(data);
//   } else {
//     let jsonStr = JSON.parse(JSON.stringify(data.toJson(password)));
//     signUrl = keyring.addFromJson(jsonStr);
//     signUrl.unlock(password);
//   }
//   const signature = signUrl.sign(nonce);
//   console.log("signature", signature, u8aToHex(signature) );
  
//   return { nonce, signature: u8aToHex(signature) };
// };


// 创建签名
export const signData = async (data, password, type) => {
  const nonce = uuidv4();
  // const nonce = "test";
  const nonceU8a = stringToU8a(nonce); // 转换为 Uint8Array
>>>>>>> fingerprintAuth-out
  let signUrl;
  await cryptoWaitReady();
  if (type == "seed") {
    signUrl = keyring.addFromUri(data);
  } else {
    let jsonStr = JSON.parse(JSON.stringify(data.toJson(password)));
    signUrl = keyring.addFromJson(jsonStr);
    signUrl.unlock(password);
  }
  // const signature = signUrl.sign(nonceU8a);
  const signature = signUrl.sign(nonceU8a);
  console.log("signature", signature, u8aToHex(signature));

<<<<<<< HEAD
  return { nonce, signature: u8aToHex(signature) }; // nonce returns as a string
=======
  return { nonce, signature: u8aToHex(signature) }; // nonce 作为字符串返回
>>>>>>> fingerprintAuth-out
};
