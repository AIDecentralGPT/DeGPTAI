
// import { Core } from '@walletconnect/core'
// import { Web3Wallet } from '@walletconnect/web3wallet'

// const core = new Core({
//   projectId: 'a365ccf6c502136ee70fd89768611fc2'
// })

// const metadata = {
//   name: 'degpt-demo',
//   description: 'AppKit Example',
//   url: 'https://web3modal.com', // origin must match your domain & subdomain
//   icons: ['https://avatars.githubusercontent.com/u/37784886']
// }


// export let web3wallet = null;


// export  async function createWalletConnect() {
//    web3wallet = await Web3Wallet.init({
//     core, // <- pass the shared 'core' instance
//     metadata
//   })


//   console.log("createWalletConnect执行了", web3wallet);
  

// }

// export async function connectWallet() {
//   if (!web3wallet) {
//     await createWalletConnect();
//   }

//   const result = await web3wallet.connect();

//   if (result) {
//     const { accounts } = result.params[0];
//     console.log("Connected accounts:", accounts);
//     return accounts[0];
//   }

//   return null;
// }

// // export async function getBalance(address) {
// //   const provider = new Web3.providers.HttpProvider(core.relayUrl);
// //   const web3 = new Web3(provider);

// //   const balance = await web3.eth.getBalance(address);
// //   return Web3.utils.fromWei(balance, 'ether');
// // }
