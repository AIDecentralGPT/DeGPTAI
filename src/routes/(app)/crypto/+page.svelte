
<script>
  let rewards = [
    {
      title: "I. New User Creation Reward",
      description: "After completing new user authentication, receive a 2000 DGC reward."
    },
    {
      title: "II. Referral Reward",
      description: [
        "1. For each friend invited to create a wallet successfully, the user receives a 1000 DGC reward, and the friend also receives a 1000 DGC reward.",
        "2. Maximum of 10 invitations per day, with a daily maximum reward of 10000 DGC."
      ]
    },
    {
      title: "III. Clock in Reward",
      description: [
        "1. Clock in reward is valid for 60 days after authentication is completed.",
        "2. Logging in and clocking in for 1 day can earn 500 DGC rewards; maximum of 30 Clock in rewards.",
        "3. User Clock in rule: log in to DEGPT every 24 hours and send a valid command once using DEGPT."
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
    <h2>{reward.title}</h2>
    {#if Array.isArray(reward.description)}
      <ul>
        {#each reward.description as desc}
          <li>{desc}</li>
        {/each}
      </ul>
    {:else}
      <p>{reward.description}</p>
    {/if}
  {/each}
</main>
