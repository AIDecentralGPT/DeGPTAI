
allowance

功能: 查询账户（owner）授权给另一个账户（spender）可以转移的代币数量。
使用方法: 调用 allowance(owner, spender) 函数，返回一个 uint256 类型的数值，表示授权的代币数量。
approve

功能: 授权一个账户（spender）可以转移不超过指定数量的代币。
使用方法: 调用 approve(spender, value) 函数，其中 spender 是被授权账户的地址，value 是授权的代币数量，返回一个 bool 类型表示操作是否成功。
balanceOf

功能: 查询指定账户（account）的代币余额。
使用方法: 调用 balanceOf(account) 函数，返回一个 uint256 类型的数值，表示指定账户的代币余额。
claimStuckTokens

功能: 提取合约中卡住的代币。
使用方法: 调用 claimStuckTokens() 函数，向合约发送交易以解锁卡住的代币。
decimals

功能: 查询代币的小数位数。
使用方法: 调用 decimals() 函数，返回一个 uint8 类型的数值，表示代币的小数位数。
initialize

功能: 初始化合约的初始拥有者。
使用方法: 调用 initialize(initialOwner) 函数，其中 initialOwner 是初始拥有者的地址，只能在合约部署后进行一次初始化。
isLockActive

功能: 查询锁定转账功能是否激活。
使用方法: 调用 isLockActive() 函数，返回一个 bool 类型表示锁定转账功能是否激活。
name

功能: 查询代币的名称。
使用方法: 调用 name() 函数，返回一个 string 类型表示代币的名称。
nonces

功能: 查询账户的交易序号（nonce）。
使用方法: 调用 nonces(account) 函数，返回一个 uint256 类型的数值，表示指定账户的交易序号。
owner

功能: 查询合约的当前所有者地址。
使用方法: 调用 owner() 函数，返回一个 address 类型表示当前合约的所有者地址。
renounceOwnership

功能: 放弃合约的所有者权限。
使用方法: 调用 renounceOwnership() 函数，向合约发送交易以放弃当前所有者权限。
symbol

功能: 查询代币的符号。
使用方法: 调用 symbol() 函数，返回一个 string 类型表示代币的符号。
totalSupply

功能: 查询代币的总供应量。
使用方法: 调用 totalSupply() 函数，返回一个 uint256 类型的数值，表示代币的总供应量。
transfer

功能: 转移指定数量的代币到另一个账户。
使用方法: 调用 transfer(to, amount) 函数，其中 to 是接收代币的账户地址，amount 是转移的代币数量，返回一个 bool 类型表示操作是否成功。
transferAndLock

功能: 转移指定数量的代币到另一个账户并锁定一段时间。
使用方法: 调用 transferAndLock(to, value, lockSeconds) 函数，其中 to 是接收代币的账户地址，value 是转移的代币数量，lockSeconds 是锁定的秒数。
transferFrom

功能: 从一个账户转移指定数量的代币到另一个账户（适用于授权后的转账）。
使用方法: 调用 transferFrom(from, to, value) 函数，其中 from 是转移代币的账户地址，to 是接收代币的账户地址，value 是转移的代币数量，返回一个 bool 类型表示操作是否成功。
transferOwnership

功能: 转移合约的所有者权限给新的账户。
使用方法: 调用 transferOwnership(newOwner) 函数，其中 newOwner 是新的合约所有者的地址，向合约发送交易以完成所有者权限的转移。
updateLockBlock

功能: 更新锁定转账的区块号。
使用方法: 调用 updateLockBlock(wallet, blockNumber) 函数，其中 wallet 是被更新的账户地址，blockNumber 是要更新的区块号，向合约发送交易以更新锁定转账的区块号。
addLockTransferAdmin

功能: 添加锁定转账管理员。
使用方法: 调用 addLockTransferAdmin(wallet) 函数，其中 wallet 是要添加为锁定转账管理员的账户地址，向合约发送交易以添加管理员权限。
disableLockPermanently

功能: 永久禁用锁定转账功能。
使用方法: 调用 disableLockPermanently() 函数，向合约发送交易以永久禁用锁定转账功能。
enableLockPermanently

功能: 永久启用锁定转账功能。
使用方法: 调用 enableLockPermanently() 函数，向合约发送交易以永久启用锁定转账功能。
eip712Domain

功能: 查询 EIP-712 域信息。
使用方法: 调用 eip712Domain() 函数，返回一个包含域信息的结构体。
DOMAIN_SEPARATOR

功能: 查询 EIP-712 域分隔符。
使用方法: 调用 DOMAIN_SEPARATOR() 函数，返回一个 bytes32 类型的数值，表示 EIP-712 域的分隔符。