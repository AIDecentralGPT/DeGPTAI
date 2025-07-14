
allowance

<<<<<<< HEAD
Function: Check the number of tokens that can be transferred from one account (owner) authorized to another account (speaker). 
Usage: Call the allowance (owner, speaker) function to return a value of type uint256 representing the number of authorized tokens.
approve

Function: Authorize an account (speaker) to transfer no more than a specified amount of tokens. 
Usage: Call the approve (speaker, value) function, where speaker is the address of the authorized account, value is the number of authorized tokens, and returns a boolean type indicating whether the operation was successful.
balanceOf

Function: Query the token balance of a specified account. 
Usage: Call the balanceOf (account) function to return a value of type uint256 representing the token balance of the specified account.
claimStuckTokens

Function: Extract tokens stuck in the contract. 
Usage: Call the claimStuckTokens() function to send a transaction to the contract to unlock the stuck token.
decimals

Function: Check the decimal places of the token. 
Usage: Call the decimal() function to return a uint8 value representing the number of decimal places in the token.
initialize

Function: Initialize the initial owner of the contract. 
Usage: Call the initialize (originalOwner) function, where originalOwner is the address of the initial owner and can only be initialized once after contract deployment.
isLockActive

Function: Check if the locked transfer function is activated. 
Usage: Call the isLockActive() function to return a boolean type indicating whether the lock transfer function is activated.
name

Function: Query the name of the token. 
Usage: Call the name() function to return a string type representing the name of the token.
nonces

Function: Check the transaction number (nonce) of the account. 
Usage: Call the nonce (account) function to return a value of type uint256 representing the transaction number of the specified account.
owner

Function: Query the current owner address of the contract. 
Usage: Call the owner() function to return an address type representing the owner address of the current contract.
renounceOwnership

Function: Abandon the ownership rights of the contract. 
Usage: Call the renouncieOwnership() function to send a transaction to the contract to relinquish the current owner's permission.
symbol

Function: Check the symbol of the token. 
Usage: Call the symbol() function to return a string type symbol representing the token.
totalSupply

Function: Check the total supply of tokens. 
Usage: Call the countSupply() function to return a value of type uint256 representing the total supply of tokens.
transfer

Function: Transfer a specified amount of tokens to another account. 
Usage: Call the transfer (to, amount) function, where to is the address of the account receiving the token, amount is the number of tokens transferred, and returns a boolean type indicating whether the operation was successful.
transferAndLock

Function: Transfer a specified amount of tokens to another account and lock it for a period of time. 
Usage: Call the transferAndLock (to, value, lockSeconds) function, where to is the account address receiving the token, value is the number of tokens transferred, and lockSeconds is the number of seconds locked.
transferFrom

Function: Transfer a specified amount of tokens from one account to another (applicable for authorized transfers). 
Usage: Call the transferFrom (from, to, value) function, where 'from' is the account address for transferring tokens, 'to' is the account address for receiving tokens, 'value' is the number of tokens transferred, and returns a boolean type indicating whether the operation was successful.
transferOwnership

Function: Transfer the owner's rights of the contract to a new account. 
Usage: Call the transferOwnership (newOwner) function, where newOwner is the address of the new contract owner, and send a transaction to the contract to complete the transfer of owner permissions.
updateLockBlock

Function: Update the block number for locked transfers. 
Usage: Call the updateLockBlock (wallet, blockNumber) function, where the wallet is the updated account address and blockNumber is the block number to be updated. Send a transaction to the contract to update the block number for the locked transfer.
addLockTransferAdmin

Function: Add a locked transfer administrator. 
Usage: Call the addLockTransferAdmin (wallet) function, where the wallet is the account address to be added as the lock transfer administrator, and send transactions to the contract to add administrator privileges.
disableLockPermanently

Function: Permanently disable the lock transfer function. 
Usage: Call the disableLockPermanently () function to send a transaction to the contract to permanently disable the lock transfer function.
enableLockPermanently

Function: Permanently enable the locked transfer function. 
Usage: Call the enableLockPermanenty() function to send a transaction to the contract to permanently enable the lock transfer function.
eip712Domain

Function: Query EIP-712 domain information. 
Usage: Call the eip712Domain() function to return a structure containing domain information.
DOMAIN_SEPARATOR

Function: Query EIP-712 domain delimiter. 
Usage: Call the DOMAIN_SPARATOR() function to return a bytes32 value representing the delimiter of the EIP-712 field.
=======
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
>>>>>>> fingerprintAuth-out
