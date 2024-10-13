<script>
  import { createWeb3Modal, defaultWagmiConfig } from "@web3modal/wagmi";
  import { mainnet, arbitrum } from "viem/chains";
  import {
    reconnect,
    configureChains,
    createClient,
    useAccount,
    useConnect,
  } from "@wagmi/core";
  import { InjectedConnector } from "@wagmi/core/connectors/injected";

  // 1. Your WalletConnect Cloud project ID
  const projectId = "a365ccf6c502136ee70fd89768611fc2";

  // 2. Create a metadata object
  const metadata = {
    name: "degpt-demo",
    description: "Web3Modal Example",
    url: "https://web3modal.com", // origin must match your domain & subdomain
    icons: ["https://avatars.githubusercontent.com/u/37784886"],
  };

  // 3. Create wagmiConfig
  const chains = [mainnet, arbitrum];
  const wagmiOptions = {
    autoConnect: true,
    connectors: [new InjectedConnector({ chains })],
  };

  const config = defaultWagmiConfig({
    chains,
    projectId,
    metadata,
    ...wagmiOptions,
  });

  const client = createClient(config);

  reconnect(config);

  // 4. Create modal
  const modal = createWeb3Modal({
    wagmiConfig: config,
    projectId,
    enableAnalytics: true, // Optional - defaults to your Cloud configuration
    enableOnramp: true, // Optional - false as default
  });

  // 5. Connect Wallet function
  const { connect } = useConnect();
  const { isConnected, address } = useAccount();
  const connecting = ref(false);

  const connectWallet = async () => {
    try {
      connecting.value = true;
      await connect({ connector: new InjectedConnector({ chains }) });
      console.log("Wallet connected", address.value);
    } catch (error) {
      console.error("Failed to connect wallet", error);
    } finally {
      connecting.value = false;
    }
  };
</script>

<div>
  <button on:click={connectWallet()}>Connect Wallet</button>
  <div>
    <p>Connected Address: {{ address }}</p>
  </div>
  <!-- Rest of your app ... -->
</div>
