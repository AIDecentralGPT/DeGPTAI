from fastapi import APIRouter, Depends, HTTPException
from apps.web.models.errorlog import ErrorLogInstance, ErrorLogRequest
from apps.web.models.faceCompare import face_compare
from apps.web.models.faceLib import face_lib
import json
import base64


router = APIRouter()

# 添加IP记录
@router.post("/add")
async def add_err_log(errlog: ErrorLogRequest):
    try:
        errorlog = ErrorLogInstance.insert_errorlog(errlog.name, errlog.err)
        return errorlog
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# 获取人脸图像
@router.get("/faceimg/{transaction_id}/{merchant_biz_id}")
async def faceimg(transaction_id: str, merchant_biz_id: str):

    transactionIds = ["hksb84647cf99b9ea970ce6f1ff34773",
        "hksa756b5ac7853c9b3638904dceb0a3",
        "hks1b2355e72d2178a58507197d3ba0d",
        "hksfb8b099c5df0bc53ef80559936737",
        "hksea964ed9af7168b2d53c9c2e96b31",
        "hksb829b1577c36242699b9d33c8b72b",
        "hksdb33a95b472f69f1df1e25ce5c220",
        "hksc7e6a0cf4392eeae60285c3ff7c7d",
        "hks487999fdc60fd7ddf7b8b6849f3f7",
        "hks20376dd97b1f5c02bc5659b37ad6f",
        "hksc4a77479ed8183eb5b1a110bdd331",
        "hks8ac793a6da0b4c15f304fbb57d9c5",
        "hksdf43302eb243545963cde2ec272cd",
        "hks0ae0449e0ce5e000da495a2f0c8a0",
        "hks2e1f2e8a0a063c6572be687c660a8",
        "hksb9e46c8397856f80faf044daa01dc",
        "hksd590ae1d00e91d4621a6959108f1a",
        "hks000829d7f169a3e865f67c037fd01",
        "hksf0bb0d66f6c644eec150b05ccffea",
        "hksb8f371c6709092e99fe56138ba0f4",
        "hks45f9b13a44aeca4e45c2c5b229dac",
        "hks762bc6314383c24effd899f402157",
        "hks4c1572f1835737eea1d2c32b9f5ab",
        "hks022465fdb5619466210da8fba3bce",
        "hksde821dea41ae7ab78c435c61841e4",
        "hks2ac51868e47706be957469526e9cc",
        "hks91ae927f35c31f77a3bb6904b6c16",
        "hkse1efe2e72e2e984f22cc295db7539",
        "hks42b1d80a1cbd7d360e29de3feefcc",
        "hks163de1b2874d074589a3016d1b8bb",
        "hks428c467ba53cdde9b8170d2261845",
        "hksd35dca8801e42991781f1ae45c979",
        "hks8d3e6477ad2c45a9f3b76a96e76a8",
        "hks48173062b94860da384db66297850",
        "hksaad217f296ff32782d9ea5c2486ee",
        "hks4a0e5cadad1bc5fcd066f07512d1b",
        "hks4e5be885185ad80bb1b50e67285d3",
        "hks9d5eaf84256f30e32f56a1d1dfa1e",
        "hkse9efa99af72a3e80f68ea75127ef1",
        "hks018090836bdf638d086668b7ecca9",
        "hksa4ac207e4ccc12cce37887eb90275",
        "hksafc1a4455aac3a4079ef03674bf59",
        "hkse47bbb1bd4bae614102132c68908f",
        "hkse8c67d8c59c54ddb757a065205a99",
        "hks3c1cc96b668efd96ef6659cfb140b",
        "hks87eb86c63f8cd8b6c973590297127",
        "hks91168e671bec8665864814639a5fe",
        "hks1268cb8150c7811dfa4756db1e08c",
        "hks6b89ed64cc215ee9d229b5ff34d54",
        "hks4cf783676ee08779544438e62a5b9",
        "hks8dc0cfa80ce1ad72b883b5cc45ae4",
        "hksdd8e5b49ff9f0ba278133193cff4b",
        "hks7caa39c353d75322de954968fd649",
        "hksbd6e44f517e72443887bb29aea762",
        "hks997aca4c7dcf33395656f3c03fcb7",
        "hksb5ff189697ac9a058f30a2dc0138d",
        "hksd2c675ed6351fa24c38dd6989bcda",
        "hksb15314d4e18ff9ea202574bea6641",
        "hksc864811a1daa03e9402323814ee25",
        "hkscc96546b9dfe21b57b1a69f6abb34",
        "hkseb6745b4da6d43884ec822f701867",
        "hks64e874d801680b4e03224d4eecb4b",
        "hks09ea5492ce6fde3db72c1f027392b",
        "hksd845623a5dc16f04170a27b30cf00",
        "hks3d3a752a7371f512a6e7e3954fa2a",
        "hksdc12c402c7aecc1ca375201cd87a6",
        "hks179a1f3cacbef57c285d6d22e5b49",
        "hksbcea0deab5cea4f8fdd7d1749ef84",
        "hks58a5e56066d61143b553931472632",
        "hks8422c0ab87854539123ac1b2e795f",
        "hks6669cfec65d4e922218588bf12a93",
        "hksf51aedb6ee3c60b3aa9c5723400ec",
        "hks96ae5ec6af7224e3c422bb59693cc",
        "hks8409536e6d50dc5eedc0af744919f",
        "hks36ded9d13bcf7c8cd1a8eb1fe1c5f",
        "hkse91d395e31ee238646bbbfe2dcd76",
        "hks6c8ae49ba01f786aa3eb4f614b9e8",
        "hkse0e96edd41e0834dc231a73cce7b1",
        "hks013967532d084c5eda3b67c7e38ff",
        "hks4bce6fa574dc612ed7cf1cbc129a8",
        "hks7f95d81c83b7b3e03b00074fb3318",
        "hks5212420093a802b5307e4e08861e0"]

    # 1. 获取人脸检测返回的信息（包含照片base64信息
    for transaction_id in transactionIds:
        response = face_compare.check_result(
            transaction_id=transaction_id,
            merchant_biz_id=merchant_biz_id,
        )

        # print("face compare success", response, response.body.result.ext_face_info, response.body)
        # print("ext_face_info",  json.loads(response.body.result.ext_face_info)['faceImg'], )

        # 2. 获取人脸照片
        faceImg = json.loads(response.body.result.ext_face_info)['faceImg']
        # 解码 Base64 字符串
        image_data = base64.b64decode(faceImg)
        # 以二进制写入模式打开文件
        output_path = f"E:/Project/zj/faceImg/{transaction_id}.png"
        with open(output_path, 'wb') as file:
            # 将解码后的数据写入文件
            file.write(image_data)
            print(f"图片已成功保存到 {output_path}")
    return faceImg

# 校验人脸图像
@router.get("/faceimg/check")
async def faceimg():
    base64 = ""
    result = face_lib.check_face_image(base64)
    return result
