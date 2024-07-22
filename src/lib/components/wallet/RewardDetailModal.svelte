<script lang="ts">
  import { toast } from "svelte-sonner";
  import Modal from "../common/Modal.svelte";
  export let show = false;
  import { onMount, getContext } from "svelte";
  const i18n = getContext("i18n");

  let rewards = [
  {
    title: "I. New User Creation Reward",
    description: "After completing new user authentication, receive a <span style='color: rgba(184, 142, 86, 1);'>2000</span> DGC reward."
  },
  {
    title: "II. Referral Reward",
    description: [
      "1. For each friend invited to create a wallet successfully, the user receives a <span style='color: rgba(184, 142, 86, 1);'>1000</span> DGC reward, and the friend also receives a <span style='color: rgba(184, 142, 86, 1);'>1000</span> DGC reward.",
      "2. Maximum of <span style='color: rgba(184, 142, 86, 1);'>10</span> invitations per day, with a daily maximum reward of <span style='color: rgba(184, 142, 86, 1);'>10000</span> DGC."
    ]
  },
  {
    title: "III. Clock in Reward",
    description: [
      "1. Clock in reward is valid for <span style='color: rgba(184, 142, 86, 1);'>60</span> days after authentication is completed.",
      "2. Logging in and clocking in for <span style='color: rgba(184, 142, 86, 1);'>1</span> day can earn <span style='color: rgba(184, 142, 86, 1);'>500</span> DGC rewards; maximum of <span style='color: rgba(184, 142, 86, 1);'>30</span> Clock in rewards.",
      "3. User Clock in rule: log in to DEGPT every <span style='color: rgba(184, 142, 86, 1);'>24</span> hours and send a valid command once using DEGPT."
    ]
  }
];

</script>

<Modal bind:show size="lg">
  <div class="max-h-[80vh] xs:h-auto flex flex-col">
    <div class=" flex justify-end dark:text-gray-300 px-5 pt-4 pb-1">
        <button
          class="self-center"
          on:click={() => {
            show = false;
          }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            class="w-5 h-5"
          >
            <path
              d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
            />
          </svg>
        </button>
      </div>

    <div class="  p-6 pt-0 shadow-md mt-0 flex-1">
      <div>
        <h1>Rewards Details</h1>
        {#each rewards as reward}
          <h2>{reward.title}</h2>
          {#if Array.isArray(reward.description)}
            <ul>
              {#each reward.description as desc}
                <li>{@html desc}</li>
              {/each}
            </ul>
          {:else}
            <p>{@html reward.description}</p>
          {/if}
        {/each}
      </div>
    </div>
  </div>
</Modal>

<style>
  h1 {
    font-size: 24px;
    margin-bottom: 16px;
  }
  h2 {
    font-size: 20px;
    margin-top: 20px;
  }
  p {
    font-size: 16px;
    margin: 8px 0;
  }
  li {
    font-size: 16px;
  }
</style>
