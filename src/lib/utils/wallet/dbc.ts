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
  dbc: "wss://info1.dbcwallet.io", // Public Chain Official Chain
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

/**
 * Initialize the connection with blockchain nodes
 * Get Polkadot API instance
 */
export const GetApi = async () => {
  if (!api) {
    const provider = new WsProvider(node.dbctest);
    api = await ApiPromise.create({ provider });
  }
  return { api };
};

// Account addition, deletion, modification, and query related

// Create an account
/**
 * Create an account using random seeds
 */
export const createAccountFromSeed = async () => {
  if (keyring) {
    await cryptoWaitReady();
    const seed = u8aToHex(randomAsU8a());
    const pair = keyring.addFromUri(seed);
    return {
      seed, // secret key
      pair, // account pairs
    };
  }
  return null;
};

/**
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
 */
export const importAccountFromSeed = async (seed) => {
  await cryptoWaitReady();
  return keyring.addFromUri(seed);
};

/**
 * Import account through JSON file
 * @param {File} file - JSON fole
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
 * Import account from JSON
 * @param {object} json - JSON object
 * @returns {object}
 */
export const importAccountFromJson = (json) => {
  if (keyring) {
    return keyring.addFromJson(json);
  }
  return null;
};

/**
 * Restore account from local storage
 * @returns {object}
 */
export const initFromLocalstorage = () => {
  const jsonStr = localStorage.getItem("pair");
  console.log("Get jsonStr locally:", jsonStr);
  
  if (keyring && jsonStr) {
    const json = JSON.parse(jsonStr);
    return importAccountFromJson(json);
  }
  return null;
};

/**
 * Export the account as a JSON file
 * @param {object} pair - account pairs
 * @param {string} password - password
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


/**
 * Save account information locally
 * @param {object} pair - account pairs
 * @param {string} password - password
 */
export const savePair = (pair, password) => {
  const jsonString = JSON.stringify(pair.toJson(password));
  console.log("jsonString", jsonString);
  localStorage.setItem("pair", jsonString);
};

/**
 * Get all account pairs
 * @returns {Array}
 */
export const getPairs = () => {
  return keyring.getPairs() || [];
};

/**
 * Obtain account pairs based on address
 * @param {string} address - Account address
 * @returns {object}
 */
export const getPair = (address) => {
  return keyring.getPair(address);
};

/**
 * Get the current account pair
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
 * Remove account pair
 * @param {string} address - Account address
 */
export const removePair = (address) => {
  keyring.removePair(address);
  localStorage.removeItem("pair");
};

// Balance related
/**
 * Get the balance of the current account
 * @param {string} address - Account address
 * @returns {object} Return balance information
 */
export const onGetBalance = async (address) => {
  await GetApi();
  const balance = await api.query.system.account(address);
  let returnData = balance.toJSON();

  console.log("balance returnData", returnData);
  

  let reserved = getFloat(returnData.data.reserved);
  let feeFrozen = getFloat(returnData.data.feeFrozen);
  let transfer = getFloat(
    Number(returnData.data.free) - Number(returnData.data.feeFrozen)
  );
  let count = getFloat(
    Number(returnData.data.free) + Number(returnData.data.reserved)
  );
  return {
    transfer,
    reserved,
    feeFrozen,
    count,
  };
};

/**
 * Get the DLC balance of the current account
 * @param {string} address - Account address
 * @returns {object} Return DLC balance information
 */
export const onGetDLCBalance = async (address) => {
  await GetApi();
  const DLCBalance = await api.query.assets.account(88, address);
  const DLCBalanceLock = await api.query.assets.assetLocks(88, address);
  const DLCBalanceTotalLock = await api.query.assets.locked(88, address);
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

// Check account balance
/**
 * Obtain account DLC and DBC balance
 * @param {string} wallet - Account address
 * @returns {object} Return balance information
 */
export const getBalanceInfo = async (wallet) => {
  await GetApi();
  const balance = await api.query.system.account(wallet);
  const returnData = balance.toJSON();
  const transfer = getFloat(
    Number(returnData.data.free) - Number(returnData.data.feeFrozen)
  );
  const DLCBalance = await api.query.assets.account(88, wallet);
  const DLCBalanceData = DLCBalance.toJSON();
  return {
    dlc_balance: DLCBalanceData
      ? Number((DLCBalanceData.balance / Math.pow(10, 8)).toFixed(4))
      : 0,
    dbc_balance: Number(transfer),
  };
};

/**
 * Transfer to DBC account
 * @param {string} address - Target DBC account address
 * @param {number} num - Transfer amount
 * @param {string} password - Account password
 * @param {function} callback - callback
 */
export const transferDBC = async (address, num, password, callback) => {
  await GetApi();
  const siPower = new BN(15);
  const bob = inputToBn(String(num), siPower, 15);
  let kering = getCurrentPair();
  try {
    kering?.unlock(password);
  } catch (e) {
    console.log("transferDBC fun", e);
    
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
      console.log("transferDBC fun", res);

      CallBack_data1 = {
        msg: res.message,
        success: false,
      };
      callback(CallBack_data1);
    });
};

/**
 * Transfer DLC
 * @param {string} address - Target DLC account address
 * @param {number} num - Transfer amount
 * @param {string} password - Account password
 * @param {function} callback - callback
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

// Get the current block height
/**
 * Get the current block height
 * @returns {number} Return block height
 */
export const onGetBlockNumber = async () => {
  await GetApi();
  const BlockNumber = await api.query.system.number();
  return BlockNumber.toJSON();
};

// View real-time prices
/**
 * Get real-time prices of DBC on the chain
 * @returns {object} Return the real-time price of DBC on the chain
 */
export const dbcPriceOcw = async () => {
  await GetApi();
  console.log("api.query", api.query);

  let de = await api.query.dbcPriceOCW.avgPrice();
  console.log("de", de);
  return de.toJSON();
};

// Transfer related
/**
 * Define callback function
 * @param {object} status - status
 * @param {Array} events - events
 * @param {function} callback - callback
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
 * Convert numbers to floating-point numbers
 * @param {number} number - number
 * @returns {string} Return floating point number
 */
const getFloat = (number) => {
  number = number / Math.pow(10, 15);
  number = Math.round(number * 10000) / 10000;
  number = Number(number).toFixed(4);
  return number;
};

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
    callback({
      success: true
    }) 
  } catch (e) {

    // Set error callback data
    CallBack_data1 = {
      msg: e.message,
      success: false,
    };
    // Call callback function and pass in error callback data
    callback(CallBack_data1);
    return;
  }
};


// utilities
/**
 * Check if the key is in Hex format
 * @param {string} seed - secret key
 * @returns {boolean}
 */
export function isHexSeed(seed) {
  return isHex(seed) && seed.length === 66;
}

/**
 * Convert input to BN
 * @param {string} input - input
 * @param {BN} siPower - accuracy
 * @param {BN} basePower - basePower
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


// Create Signature
export const signData = async (data, password, type) => {
  const nonce = uuidv4();
  // const nonce = "test";
  const nonceU8a = stringToU8a(nonce); // Convert to Uint8Array
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

  return { nonce, signature: u8aToHex(signature) }; // nonce returns as a string
};
