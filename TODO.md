cookie如下：
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




storage如下：
{
    "lang": "zh-CN",
    "locale": "en-US",
    "isWhitelist": "false",
    "visitor_id": "ad1348b3a0276c860013509bcac7b9fd",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImFkMTM0OGIzYTAyNzZjODYwMDEzNTA5YmNhYzdiOWZkIiwiZXhwIjoxNzI1NjE5MDU4fQ.E-tEBm9ldSWAjQmdvUhMi9na6kHKcO-2HeeiapvhhiE"
}



SessionStorage如下：
{
    "sveltekit:scroll": "{\"1725014256622\":{\"x\":0,\"y\":0}}",
    "sveltekit:snapshot": "{}"
}






新建钱包后，unlocking完要等walletsignin执行完毕
领取奖励的操作，要有message和success文案
转账失败，也报 转账成功了。要修改
登录面板两个都有，要看一下咋回事


Clock In的时候加上loading
为什么奖励里面有两次 new wallet
Creating的时候，加上 灰色背景




测试邀请，能否得到奖励

自定义钱包，转账有问题，（购买的时候）
购买的时候加上loading


发放奖励，邀请要限制十个人



2.5    钱包余额有钱，点击upgrade。没反应。
 
2.6  转账之后，没法直接看见dbc和dgc的状态，网站刷新了之后，没法直接看见钱包余额，还需要再次open wallet(蒋道理看下，是否已解决)

2.7 电脑上dgc转不出去，dbc倒是可以的。（已解决）

2.8  考虑增加转账记录，包括接收和发送。





0xf8480ef111cfee4049410b0ad15411ada0d999121b96f8fbdc6212cd11fbb11d








1. 模型选择，vip选择后，如何还原？是还原还是怎么办

2. 邀请链接进去的时候，自动登录了三方钱包。（检测到是邀请链接，不要自动登录三方钱包）
3. 邀请后没生效？没在列表中

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

这里有问题，在三方钱包登录的时候，不能这么签名是不是，好像也可以



4. 这里添加邀请人的时候，扯到新逻辑（要交互之类的）。 可以先本地存一下localstorage，然后发请求的时候，判断一下，然后发送添加邀请请求

5. 登录多个钱包。如何处理？

6. 加上首页的各个按钮

8. 钱包登录的时候，现在的逻辑不适应于 三方钱包







7. 奖励的是dbc现在





















# 问题：
问产品： 不需要查看转账记录吗
换掉邀请链接


# TODO
1. https://www.degpt.ai?invite=Cruj9oS5NO 邀请链接要更新，新邀请的要写入数据库等相关逻辑，邀请奖励相关逻辑补充
2. 购买逻辑的补充，目前钱包购买
4. dlc改名dgc，dgc的api对接（余额，转账）
5. 还有个有浏览用户超过五次。要提醒。
6. 生产环境的兼容问题先同步下
8. 

  LIama3 70B
LIama3 400B
MiniCPM-Llama3-V 2.5
Qwen2-72B
yi1.5-34B
Falcon2 11B   OpenBioLLM-Llama3 70B
400B的先不弄,优先Qwen2-72B

9. 邀请奖励规则，在rewards里显示已邀请成功链接。避免羊毛乱领奖励，所以应该有个机制限制同一台电脑活IP多次领取奖励1.邀请好友创建钱包成功，获得500个DGC奖励，好友获得500个DGC
奖励2.好友在DeepLink购买NFT，可获得10%DGC佣金奖励3.好友在DeepLink购买DGC，可获得10%DGC佣金奖励
10. DGC购买plus会员后逻辑，右侧对应文案要改下，后面加几个…以后还会更新前四个模型都是免费的，后面2个是plus会员
yi1.5-34B
_lama3 70BQwen2-72BMiniCPM-Llama3-V 2.5
lama3 400B

Falcon2 11B
   



# 完成
1. 加上三个icon，跳转到社媒
2. 能不能刚进去默认就选一个。然后要互斥()
3. 钱包登录的逻辑还没打通，新增id为钱包address，删除原来的指纹登录的所有chats
3. 多种语言的兼容， 多种主题的兼容（多语言是兼容所有还是中英日，是否需要补全），
4. 移动端的主题色的处理
导出钱包，密码对不上
5. 


   


# 数据库变更
User 添加inviter_id， str
ip_log和device表格



General Large Model Qwen2-72B，感叹号里文案: 27 language support, surpport long texts of up to 128 tokens
General Large Model  LIama3 70B,已有
General Large Model  Yi1.5-34B 已有，感叹号里文案：Powerful encoding, and instruction-following capabilities

Code Large Model  Codestral，感叹号里文案：Code completion and generation, error detection and repair
Multimodal  Large Model MiniCPM-Llama3-V 2.5，感叹号里文案： multilingual support
Medical Large Model  OpenBioLLM-Llama3 70B，感叹号里文案： Biomedical application



# TODO

unlock变颜色有延迟
有问题的改成coming soon




