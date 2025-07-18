from apps.web.models.users import UserModel

class UserUtil:
  # 校验用户角色
  def checkRole(self, user: UserModel):
    userrole = "user"
    if user.id.startswith("0x"):
      userrole = "wallet"
      if user.verified:
        userrole = "kyc"
    return userrole
  

# 实例化UserUtil类
UserUtils = UserUtil()