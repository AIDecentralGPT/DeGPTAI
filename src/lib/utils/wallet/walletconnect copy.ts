
// // main.ts

// import { createWeb3Modal, defaultWagmiConfig } from '@web3modal/wagmi'

// import { mainnet, arbitrum } from 'viem/chains'
// import { reconnect } from '@wagmi/core'

// // Your WalletConnect Cloud project ID
// export const projectId = 'a365ccf6c502136ee70fd89768611fc2'

// // Create a metadata object
// const metadata = {
//   name: 'degpt-demo',
//   description: 'Web3Modal Example',
//   url: 'https://web3modal.com', // origin must match your domain & subdomain
//   icons: ['https://avatars.githubusercontent.com/u/37784886']
// }

// // Create wagmiConfig
// const chains = [mainnet, arbitrum] as const
// export const config = defaultWagmiConfig({
//   chains,
//   projectId,
//   metadata,
//   // ...wagmiOptions // Optional - Override createConfig parameters
// })
// reconnect(config)

// const modal = createWeb3Modal({
//   wagmiConfig: config,
//   projectId,
//   enableAnalytics: true, // Optional - defaults to your Cloud configuration
//   enableOnramp: true // Optional - false as default
// })

// export  default modal





import { createWeb3Modal, defaultConfig } from '@web3modal/ethers'

// 1. Your WalletConnect Cloud project ID
export const projectId = '59443aa943b8865491317c04a19a8be3'

// 2. Set chains
const mainnet = {
  chainId: 1,
  name: 'DBC',
  currency: 'DBC',
  explorerUrl: 'https://blockscout-testnet.dbcscan.io',
  rpcUrl: 'https://rpc-testnet.dbcwallet.io'
}

// 3. Create your application's metadata object
const metadata = {
  name: 'degpt',
  description: 'AppKit Example',
  url: 'https://web3modal.com', // origin must match your domain & subdomain
  icons: ['https://avatars.githubusercontent.com/u/37784886']
}

// 4. Create Ethers config
const ethersConfig = defaultConfig({
  /*Required*/
  metadata,

  /*Optional*/
  enableEIP6963: true, // true by default
  enableInjected: true, // true by default
  enableCoinbase: true, // true by default
  rpcUrl: '...', // used for the Coinbase SDK
  defaultChainId: 1, // used for the Coinbase SDK
})

// 5. Create a Web3Modal instance
const modal = createWeb3Modal({
  ethersConfig,
  chains: [mainnet],
  projectId,
  enableAnalytics: true, // Optional - defaults to your Cloud configuration
  enableOnramp: true // Optional - false as default
})

export  default modal
