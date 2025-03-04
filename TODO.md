cookie as follows：
[
    {
        "domain": ".degpt.ai",
        "expirationDate": 1759574258.848172,
        "hostOnly": false,
        "httpOnly": false,
        "name": "_ga",
        "path": "/",
        "sameSite": null,
        "secure": false,
        "session": false,
        "storeId": null,
        "value": "GA1.1.302287857.1719481050"
    },
    {
        "domain": ".degpt.ai",
        "expirationDate": 1759574258.853168,
        "hostOnly": false,
        "httpOnly": false,
        "name": "_ga_ELT9ER83T2",
        "path": "/",
        "sameSite": null,
        "secure": false,
        "session": false,
        "storeId": null,
        "value": "GS1.1.1725014258.78.0.1725014258.0.0.0"
    }
]




storage as follows：
{
    "lang": "zh-CN",
    "locale": "en-US",
    "isWhitelist": "false",
    "visitor_id": "ad1348b3a0276c860013509bcac7b9fd",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImFkMTM0OGIzYTAyNzZjODYwMDEzNTA5YmNhYzdiOWZkIiwiZXhwIjoxNzI1NjE5MDU4fQ.E-tEBm9ldSWAjQmdvUhMi9na6kHKcO-2HeeiapvhhiE"
}



SessionStorage as follows：
{
    "sveltekit:scroll": "{\"1725014256622\":{\"x\":0,\"y\":0}}",
    "sveltekit:snapshot": "{}"
}






After creating a new wallet, unlock it and wait for walletsignin to complete its execution 
The process of receiving rewards requires message and success captions 
The transfer failed, but it was also reported as successful. To modify 
There are both login panels, we need to see what's going on


Add loading when Clock In 
Why are there two new wallets in the reward 
When creating, add a gray background




Test invitation, can you receive rewards

Custom wallet, transfer issue, (when purchasing) 
Add loading when purchasing  



Distribute rewards and limit invitations to ten people



2.5 Wallet balance is available, click upgrade. No response. 
  
After transferring 

2.6, it is not possible to directly see the status of dbc and dgc. After refreshing the website, it is not possible to directly see the wallet balance, and it is necessary to open the wallet again (Jiang Li should check if this has been resolved) 
2.7 DGC cannot be converted on the computer, but DBC can. (Resolved) 
2.8 Consider adding transfer records, including receiving and sending.





0xf8480ef111cfee4049410b0ad15411ada0d999121b96f8fbdc6212cd11fbb11d








1. Model selection, how to restore after VIP selection? Should I restore or what should I do 
2.When inviting the link, the third-party wallet was automatically logged in. (Detected as an invitation link, do not automatically log in to third-party wallets) 
3. Did the invitation not take effect? Not in the list

 async function handleWalletSignIn(walletImported: any, password: string, inviterId?:string) {
  // const { nonce, signature } = await signData(pair, password, undefined);

  // console.log("pair, password", pair, password);

    const signature = await signChallenge(walletImported, prefixedMessage);
  console.log("Signature:", signature);
  
  const walletSignInResult = await walletSignIn({
    address: walletImported?.address,
    nonce: prefixedMessage,
    device_id: localStorage.visitor_id ,
    // data: pair,
    signature,
    id: localStorage.visitor_id,
    inviter_id: inviterId
  });

There is a problem here. When logging in to the third-party wallet, you cannot sign like this, right? It seems that it is also possible



4.When adding invitees here, it comes to new logic (such as interaction). You can first save the local storage locally, and then when making a request, check and send an invitation request to add it 
5. Log in to multiple wallets. How to handle it? 
6. Add various buttons on the homepage 
7. The reward is DBC now
8.When logging into the wallet, the current logic is not suitable for third-party wallets





























# Problem：
Product inquiry: Do I not need to view transfer records 
Replace the invitation link


# TODO
1. https://www.degpt.ai?invite=Cruj9oS5NO The invitation link needs to be updated, new invitations need to be written into the database and other related logic, and the invitation reward related logic needs to be supplemented
2. Supplement to the purchasing logic, currently available for wallet purchases 
4. Change DLC to DGC and integrate DGC APIs (balance, transfer) 
5. There is also a user who has browsed more than five times. To remind. 
6. Regarding compatibility issues in the production environment, please synchronize them first
8. 

  LIama3 70B
LIama3 400B
MiniCPM-Llama3-V 2.5
Qwen2-72B
yi1.5-34B
Falcon2 11B   OpenBioLLM-Llama3 70B
Don't deal with 400B first, give priority to Qwen2-72B

9. Invitation reward rules, display the successfully invited link in rewards. To prevent wool from randomly claiming rewards, there should be a mechanism to limit the same computer's active IP from claiming rewards multiple times. 1. Invite friends to create wallets successfully and receive 500 DGC rewards, and friends will receive 500 DGC rewards 
Reward 2. Friends who purchase NFTs on DeepLink can receive a 10% DGC commission reward. 3. Friends who purchase DGCs on DeepLink can receive a 10% DGC commission reward 
10. After DGC purchases Plus membership, the corresponding text on the right needs to be modified, and a few more should be added at the end... The first four models will be updated for free, while the last two will be Plus membership
yi1.5-34B
_lama3 70BQwen2-72BMiniCPM-Llama3-V 2.5
lama3 400B

Falcon2 11B
   



# Complete
1. Add three icons to redirect to social media 
2. Can you choose one by default as soon as you enter. Then it needs to be mutually exclusive 
3. The logic of wallet login has not been established yet. Add the ID as wallet address and delete all chats logged in with the original fingerprint 
3. Compatibility with multiple languages and themes (whether multiple languages are compatible with all or Chinese, English, and Japanese, and whether completion is required), 
4. Processing of theme colors on mobile devices 
Export wallet, password does not match
5. 


   


# Database changes
User adds inviter_id, str 
Ip_rog and device table



General Large Model Qwen2-72B，Text in exclamation mark: 27 language support, surpport long texts of up to 128 tokens
General Large Model  LIama3 70B,have
General Large Model  Yi1.5-34B have，Text in exclamation mark：Powerful encoding, and instruction-following capabilities

Code Large Model  Codestral，Text in exclamation mark：Code completion and generation, error detection and repair
Multimodal  Large Model MiniCPM-Llama3-V 2.5，Text in exclamation mark： multilingual support
Medical Large Model  OpenBioLLM-Llama3 70B，Text in exclamation mark： Biomedical application



# TODO

unlock there is a delay in changing colors
Change the problematic ones to coming soon




