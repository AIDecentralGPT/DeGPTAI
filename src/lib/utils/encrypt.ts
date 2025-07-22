import { stringToU8a, u8aToHex, hexToU8a, u8aConcat } from '@polkadot/util';
import { 
  naclEncrypt, 
  naclDecrypt, 
  blake2AsU8a,
  randomAsU8a 
} from '@polkadot/util-crypto';

/**
 * 增强密钥派生（加盐防彩虹表攻击）
 */
function deriveSecureKey(key: string, salt?: Uint8Array): Uint8Array {
  const saltU8a = salt || randomAsU8a(16); // 16字节随机盐
  const keyMaterial = u8aConcat(stringToU8a(key), saltU8a);
  return blake2AsU8a(keyMaterial, 256); // 始终返回32字节密钥
}

/**
 * 增强密钥派生（加盐防彩虹表攻击）
 */
export const encryptPrivateKey = async(privateKey: string, password: string) => {
  // 生成随机盐（增强密钥派生安全性）
  const salt = randomAsU8a(16);
  // 派生加密密钥
  const derivedKey = deriveSecureKey(password, salt);
  
  // 使用Nacl加密（nonce会自动生成）
  const { encrypted, nonce } = naclEncrypt(stringToU8a(privateKey), derivedKey);
  
  // 拼接格式：salt(16) + nonce(24) + encrypted(n)
  return u8aToHex(u8aConcat(salt, nonce, encrypted));
}

/**
 * 解密私钥
 */
export const decryptPrivateKey = async (encryptedHex: string, password: string) => {
  const encryptedU8a = hexToU8a(encryptedHex);
  
  // 解析数据：salt(16) + nonce(24) + encrypted(n)
  if (encryptedU8a.length <= 40) { // 16+24=40
    throw new Error('Invalid encrypted data');
  }
  
  const salt = encryptedU8a.slice(0, 16);
  const nonce = encryptedU8a.slice(16, 40); // 16+24=40
  const encrypted = encryptedU8a.slice(40);
  
  // 重新派生密钥
  const derivedKey = deriveSecureKey(password, salt);
  
  // 解密
  const decrypted = naclDecrypt(encrypted, nonce, derivedKey);
  if (!decrypted) {
    throw new Error('Decryption failed - wrong password or corrupted data');
  }
  
  return new TextDecoder().decode(decrypted);
}