
<script>
  import { getContext } from "svelte";
  import { RewardProperties } from "$lib/constants"
  const i18n = getContext("i18n");
  let rewards = [
    {
      title: "I. New User Creation Reward",
      description: "After completing new user authentication, receive a <span style='color: rgba(184, 142, 86, 1);'>{{regist}}</span> DGC reward."
    },
    {
      title: "II. Referral Reward",
      description: "Each user who successfully creates a wallet and invites others to create a KYC wallet will receive a <span style='color: rgba(184, 142, 86, 1);'>3000</span> DGC reward."
    },
    {
      title: "III. Clock in Reward",
      description: [
        "Check in reward is valid for <span style='color: rgba(184, 142, 86, 1);'>{{civalid}}</span> days after authentication is completed.",
        "Logging in and clocking in for <span style='color: rgba(184, 142, 86, 1);'>1</span> day can earn <span style='color: rgba(184, 142, 86, 1);'>{{clockin}}</span> DGC rewards; maximum of <span style='color: rgba(184, 142, 86, 1);'>{{citimes}}</span> Clock in rewards.",
      ]
    }
  ];
</script>

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

  .document-wrap {
    
  }
</style>

<main class=" m-4 lg:mx-[40px]">
  <h1>Reward Details</h1>
  {#each rewards as reward}
    <h2>{$i18n.t(reward.title)}</h2>
    {#if Array.isArray(reward.description)}
      <ul>
        {#each reward.description as desc, index}
          <li>{index + 1}. {$i18n.t(desc, RewardProperties)}</li>
        {/each}
      </ul>
    {:else}
      <p>{$i18n.t(reward.description, RewardProperties)}</p>
    {/if}
  {/each}
</main>
