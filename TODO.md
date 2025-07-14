<<<<<<< HEAD
cookie as follows：
=======
cookie如下：
>>>>>>> fingerprintAuth-out
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




<<<<<<< HEAD
storage as follows：
=======
storage如下：
>>>>>>> fingerprintAuth-out
{
    "lang": "zh-CN",
    "locale": "en-US",
    "isWhitelist": "false",
    "visitor_id": "ad1348b3a0276c860013509bcac7b9fd",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImFkMTM0OGIzYTAyNzZjODYwMDEzNTA5YmNhYzdiOWZkIiwiZXhwIjoxNzI1NjE5MDU4fQ.E-tEBm9ldSWAjQmdvUhMi9na6kHKcO-2HeeiapvhhiE"
}



<<<<<<< HEAD
SessionStorage as follows：
=======
SessionStorage如下：
>>>>>>> fingerprintAuth-out
{
    "sveltekit:scroll": "{\"1725014256622\":{\"x\":0,\"y\":0}}",
    "sveltekit:snapshot": "{}"
}






<<<<<<< HEAD
After creating a new wallet, unlock it and wait for walletsignin to complete its execution 
The process of receiving rewards requires message and success captions 
The transfer failed, but it was also reported as successful. To modify 
There are both login panels, we need to see what's going on


Add loading when Clock In 
Why are there two new wallets in the reward 
When creating, add a gray background
=======
新建钱包后，unlocking完要等walletsignin执行完毕
领取奖励的操作，要有message和success文案
转账失败，也报 转账成功了。要修改
登录面板两个都有，要看一下咋回事


Clock In的时候加上loading
为什么奖励里面有两次 new wallet
Creating的时候，加上 灰色背景
>>>>>>> fingerprintAuth-out




<<<<<<< HEAD
Test invitation, can you receive rewards

Custom wallet, transfer issue, (when purchasing) 
Add loading when purchasing  



Distribute rewards and limit invitations to ten people



2.5 Wallet balance is available, click upgrade. No response. 
  
After transferring 

2.6, it is not possible to directly see the status of dbc and dgc. After refreshing the website, it is not possible to directly see the wallet balance, and it is necessary to open the wallet again (Jiang Li should check if this has been resolved) 
2.7 DGC cannot be converted on the computer, but DBC can. (Resolved) 
2.8 Consider adding transfer records, including receiving and sending.
=======
测试邀请，能否得到奖励

自定义钱包，转账有问题，（购买的时候）
购买的时候加上loading


发放奖励，邀请要限制十个人



2.5    钱包余额有钱，点击upgrade。没反应。
 
2.6  转账之后，没法直接看见dbc和dgc的状态，网站刷新了之后，没法直接看见钱包余额，还需要再次open wallet(蒋道理看下，是否已解决)

2.7 电脑上dgc转不出去，dbc倒是可以的。（已解决）

2.8  考虑增加转账记录，包括接收和发送。
>>>>>>> fingerprintAuth-out





0xf8480ef111cfee4049410b0ad15411ada0d999121b96f8fbdc6212cd11fbb11d








<<<<<<< HEAD
1. Model selection, how to restore after VIP selection? Should I restore or what should I do 
2.When inviting the link, the third-party wallet was automatically logged in. (Detected as an invitation link, do not automatically log in to third-party wallets) 
3. Did the invitation not take effect? Not in the list
=======
1. 模型选择，vip选择后，如何还原？是还原还是怎么办

2. 邀请链接进去的时候，自动登录了三方钱包。（检测到是邀请链接，不要自动登录三方钱包）
3. 邀请后没生效？没在列表中
>>>>>>> fingerprintAuth-out

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

<<<<<<< HEAD
There is a problem here. When logging in to the third-party wallet, you cannot sign like this, right? It seems that it is also possible



4.When adding invitees here, it comes to new logic (such as interaction). You can first save the local storage locally, and then when making a request, check and send an invitation request to add it 
5. Log in to multiple wallets. How to handle it? 
6. Add various buttons on the homepage 
7. The reward is DBC now
8.When logging into the wallet, the current logic is not suitable for third-party wallets
=======
这里有问题，在三方钱包登录的时候，不能这么签名是不是，好像也可以



4. 这里添加邀请人的时候，扯到新逻辑（要交互之类的）。 可以先本地存一下localstorage，然后发请求的时候，判断一下，然后发送添加邀请请求

5. 登录多个钱包。如何处理？

6. 加上首页的各个按钮

8. 钱包登录的时候，现在的逻辑不适应于 三方钱包







7. 奖励的是dbc现在
>>>>>>> fingerprintAuth-out





















<<<<<<< HEAD








# Problem：
Product inquiry: Do I not need to view transfer records 
Replace the invitation link


# TODO
1. https://www.degpt.ai?invite=Cruj9oS5NO The invitation link needs to be updated, new invitations need to be written into the database and other related logic, and the invitation reward related logic needs to be supplemented
2. Supplement to the purchasing logic, currently available for wallet purchases 
4. Change DLC to DGC and integrate DGC APIs (balance, transfer) 
5. There is also a user who has browsed more than five times. To remind. 
6. Regarding compatibility issues in the production environment, please synchronize them first
=======
# 问题：
问产品： 不需要查看转账记录吗
换掉邀请链接


# TODO
1. https://www.degpt.ai?invite=Cruj9oS5NO 邀请链接要更新，新邀请的要写入数据库等相关逻辑，邀请奖励相关逻辑补充
2. 购买逻辑的补充，目前钱包购买
4. dlc改名dgc，dgc的api对接（余额，转账）
5. 还有个有浏览用户超过五次。要提醒。
6. 生产环境的兼容问题先同步下
>>>>>>> fingerprintAuth-out
8. 

  LIama3 70B
LIama3 400B
MiniCPM-Llama3-V 2.5
Qwen2-72B
yi1.5-34B
Falcon2 11B   OpenBioLLM-Llama3 70B
<<<<<<< HEAD
Don't deal with 400B first, give priority to Qwen2-72B

9. Invitation reward rules, display the successfully invited link in rewards. To prevent wool from randomly claiming rewards, there should be a mechanism to limit the same computer's active IP from claiming rewards multiple times. 1. Invite friends to create wallets successfully and receive 500 DGC rewards, and friends will receive 500 DGC rewards 
Reward 2. Friends who purchase NFTs on DeepLink can receive a 10% DGC commission reward. 3. Friends who purchase DGCs on DeepLink can receive a 10% DGC commission reward 
10. After DGC purchases Plus membership, the corresponding text on the right needs to be modified, and a few more should be added at the end... The first four models will be updated for free, while the last two will be Plus membership
=======
400B的先不弄,优先Qwen2-72B

9. 邀请奖励规则，在rewards里显示已邀请成功链接。避免羊毛乱领奖励，所以应该有个机制限制同一台电脑活IP多次领取奖励1.邀请好友创建钱包成功，获得500个DGC奖励，好友获得500个DGC
奖励2.好友在DeepLink购买NFT，可获得10%DGC佣金奖励3.好友在DeepLink购买DGC，可获得10%DGC佣金奖励
10. DGC购买plus会员后逻辑，右侧对应文案要改下，后面加几个…以后还会更新前四个模型都是免费的，后面2个是plus会员
>>>>>>> fingerprintAuth-out
yi1.5-34B
_lama3 70BQwen2-72BMiniCPM-Llama3-V 2.5
lama3 400B

Falcon2 11B
   



<<<<<<< HEAD
# Complete
1. Add three icons to redirect to social media 
2. Can you choose one by default as soon as you enter. Then it needs to be mutually exclusive 
3. The logic of wallet login has not been established yet. Add the ID as wallet address and delete all chats logged in with the original fingerprint 
3. Compatibility with multiple languages and themes (whether multiple languages are compatible with all or Chinese, English, and Japanese, and whether completion is required), 
4. Processing of theme colors on mobile devices 
Export wallet, password does not match
=======
# 完成
1. 加上三个icon，跳转到社媒
2. 能不能刚进去默认就选一个。然后要互斥()
3. 钱包登录的逻辑还没打通，新增id为钱包address，删除原来的指纹登录的所有chats
3. 多种语言的兼容， 多种主题的兼容（多语言是兼容所有还是中英日，是否需要补全），
4. 移动端的主题色的处理
导出钱包，密码对不上
>>>>>>> fingerprintAuth-out
5. 


   


<<<<<<< HEAD
# Database changes
User adds inviter_id, str 
Ip_rog and device table



General Large Model Qwen2-72B，Text in exclamation mark: 27 language support, surpport long texts of up to 128 tokens
General Large Model  LIama3 70B,have
General Large Model  Yi1.5-34B have，Text in exclamation mark：Powerful encoding, and instruction-following capabilities

Code Large Model  Codestral，Text in exclamation mark：Code completion and generation, error detection and repair
Multimodal  Large Model MiniCPM-Llama3-V 2.5，Text in exclamation mark： multilingual support
Medical Large Model  OpenBioLLM-Llama3 70B，Text in exclamation mark： Biomedical application
=======
# 数据库变更
User 添加inviter_id， str
ip_log和device表格



General Large Model Qwen2-72B，感叹号里文案: 27 language support, surpport long texts of up to 128 tokens
General Large Model  LIama3 70B,已有
General Large Model  Yi1.5-34B 已有，感叹号里文案：Powerful encoding, and instruction-following capabilities

Code Large Model  Codestral，感叹号里文案：Code completion and generation, error detection and repair
Multimodal  Large Model MiniCPM-Llama3-V 2.5，感叹号里文案： multilingual support
Medical Large Model  OpenBioLLM-Llama3 70B，感叹号里文案： Biomedical application
>>>>>>> fingerprintAuth-out



# TODO

<<<<<<< HEAD
unlock there is a delay in changing colors
Change the problematic ones to coming soon
=======
unlock变颜色有延迟
有问题的改成coming soon
>>>>>>> fingerprintAuth-out




