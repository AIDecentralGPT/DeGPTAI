import { createConfig, http } from '@wagmi/core';
import { mainnet, bsc } from '@wagmi/core/chains';
import { injected } from '@wagmi/connectors';

// 创建配置
export const config = createConfig({
  chains: [mainnet, bsc],
  transports: {
    [mainnet.id]: http(),
    [bsc.id]: http(),
  },
  connectors: [
    injected({
      target: 'metaMask', // 明确声明目标钱包，增强兼容性
    }),
  ],
});