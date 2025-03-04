
allowance

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