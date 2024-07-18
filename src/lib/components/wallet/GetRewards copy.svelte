<script lang="ts">
  import {
    exportAccountForKeystore,
    createAccountFromMnemonic,
    createAccountFromSeed,
    getCurrentPair,
    savePair,
  } from "./../../utils/wallet/dbc.js";
  import { getContext, onMount } from "svelte";
  import { toast } from "svelte-sonner";

  import { getModels as _getModels } from "$lib/utils";

  import Modal from "../common/Modal.svelte";
  import { onGetBalance } from "$lib/utils/wallet/dbc.js";
  import { onGetDLCBalance } from "$lib/utils/wallet/dbc.js";
  import { currentWalletData, models, settings, user, inviterId } from "$lib/stores";
  import { createAccount, downloadKeyStore } from "$lib/utils/wallet/ether/utils.js";

  const i18n = getContext("i18n");


</script>

<div class="flex justify-between items-center ">

  <!-- <div class="flex justify-center items-center flex-col" >
    
    <svg
    class=" text-yellow-600 "
    
    xmlns="http://www.w3.org/2000/svg" width="3em" height="3em" viewBox="0 0 24 24"><path fill="currentColor" d="M6 20q-1.65 0-2.825-1.175T2 16V8q0-1.65 1.175-2.825T6 4h12q1.65 0 2.825 1.175T22 8v8q0 1.65-1.175 2.825T18 20zM6 8h12q.55 0 1.05.125t.95.4V8q0-.825-.587-1.412T18 6H6q-.825 0-1.412.588T4 8v.525q.45-.275.95-.4T6 8m-1.85 3.25l11.125 2.7q.225.05.45 0t.425-.2l3.475-2.9q-.275-.375-.7-.612T18 10H6q-.65 0-1.137.338t-.713.912"/></svg>
    
  <span class="">Create Wallet</span>
  </div> -->


  <div class="flex justify-between items-center gap-2" >
    <svg
    xmlns="http://www.w3.org/2000/svg" width="2em" height="2em" viewBox="0 0 24 24"><path fill="currentColor" d="M6 20q-1.65 0-2.825-1.175T2 16V8q0-1.65 1.175-2.825T6 4h12q1.65 0 2.825 1.175T22 8v8q0 1.65-1.175 2.825T18 20zM6 8h12q.55 0 1.05.125t.95.4V8q0-.825-.587-1.412T18 6H6q-.825 0-1.412.588T4 8v.525q.45-.275.95-.4T6 8m-1.85 3.25l11.125 2.7q.225.05.45 0t.425-.2l3.475-2.9q-.275-.375-.7-.612T18 10H6q-.65 0-1.137.338t-.713.912"/></svg>
    
  <span class="">1. Create Wallet</span>
  </div>
  <div
				
				class=" px-4 py-2 primaryButton text-gray-100 transition rounded-lg"
			>



				<span class="relative">2000DGCs</span>
        <button
        class=" px-4 py-2 dark:bg-white dark:text-zinc-950 bg-black text-gray-100 transition rounded-lg"
        >
          Get Now!
        </button>
			</div>

</div>
