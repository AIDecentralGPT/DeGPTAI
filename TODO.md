
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


   


# 数据库变更
User 添加inviter_id， str
ip_log和device表格