// import { ethers } from "ethers";

// // 连接 DBC Testnet
// const ALCHEMY_TESTNET_URL = 'https://rpc-testnet.dbcwallet.io';

// export async function main() {
//   const provider = new ethers.JsonRpcProvider(ALCHEMY_TESTNET_URL);

//   // 使用以太坊地址而不是 ENS 名称
//   const address = '0xde184A6809898D81186DeF5C0823d2107c001Da2'; // 这是一个示例地址，请替换为实际地址

//   const balance = await provider.getBalance(address);
//   // 转换单位后在 console 中输出
//   console.log(`ETH Balance of ${address}: ${ethers.formatEther(balance)} DGC`);
// }

// main();




import { ethers } from "ethers";

// 连接 DBC Testnet
const ALCHEMY_TESTNET_URL = 'https://rpc-testnet.dbcwallet.io';

export async function main() {
  const provider = new ethers.JsonRpcProvider(ALCHEMY_TESTNET_URL);

  const address = '0xde184A6809898D81186DeF5C0823d2107c001Da2'; // 这是一个示例地址，请替换为实际地址

  // DBC 和 DGC 的合约地址
  const TOKEN_CONTRACT_ADDRESS = '0x82b1a3d719dDbFDa07AD1312c3063a829e1e66F1'; // 请替换为实际地址

  // ERC-20 ABI
  const ERC20_ABI = [
    "function balanceOf(address owner) view returns (uint256)",
    "function symbol() view returns (string)",
    "function decimals() view returns (uint8)"
  ];

  // 创建合约实例
  const tokenContract = new ethers.Contract(TOKEN_CONTRACT_ADDRESS, ERC20_ABI, provider);

  // 查询代币符号和小数位
  const symbol = await tokenContract.symbol();
  const decimals = await tokenContract.decimals();

  // 查询代币余额
  const balance = await tokenContract.balanceOf(address);
  console.log(`${symbol} Balance of ${address}: ${ethers.formatUnits(balance, decimals)} ${symbol}`);

  // 查询 余额
  const dbcBalance = await provider.getBalance(address);
  console.log(`DBC Balance of ${address}: ${ethers.formatEther(dbcBalance)} DBC`);
}