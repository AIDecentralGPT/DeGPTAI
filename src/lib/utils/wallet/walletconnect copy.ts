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
