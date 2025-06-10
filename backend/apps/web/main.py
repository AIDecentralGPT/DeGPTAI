from fastapi import FastAPI, Depends
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from apps.web.routers import (
    auths,
    users,
    chats,
    documents,
    modelfiles,
    prompts,
    configs,
    memories,
    utils,
    device,
    ip_log,
    rewards,
    reward_date,
    conversation,
    third,
    kycrestrict,
    error_log,
    mcphttp,
    completion
)
from config import (
    WEBUI_VERSION,
    WEBUI_AUTH,
    DEFAULT_MODELS,
    DEFAULT_PROMPT_SUGGESTIONS,
    DEFAULT_USER_ROLE,
    ENABLE_SIGNUP,
    USER_PERMISSIONS,
    WEBHOOK_URL,
    WEBUI_AUTH_TRUSTED_EMAIL_HEADER,
    JWT_EXPIRES_IN,
    AppConfig,
)

app = FastAPI()

origins = ["*"]

app.state.config = AppConfig()

app.state.config.ENABLE_SIGNUP = ENABLE_SIGNUP
app.state.config.JWT_EXPIRES_IN = JWT_EXPIRES_IN

app.state.config.DEFAULT_MODELS = DEFAULT_MODELS
app.state.config.DEFAULT_PROMPT_SUGGESTIONS = DEFAULT_PROMPT_SUGGESTIONS
app.state.config.DEFAULT_USER_ROLE = DEFAULT_USER_ROLE
app.state.config.USER_PERMISSIONS = USER_PERMISSIONS
app.state.config.WEBHOOK_URL = WEBHOOK_URL
app.state.AUTH_TRUSTED_EMAIL_HEADER = WEBUI_AUTH_TRUSTED_EMAIL_HEADER


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auths.router, prefix="/auths", tags=["auths"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(chats.router, prefix="/chats", tags=["chats"])

app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(modelfiles.router, prefix="/modelfiles", tags=["modelfiles"])
app.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
app.include_router(memories.router, prefix="/memories", tags=["memories"])


app.include_router(configs.router, prefix="/configs", tags=["configs"])
app.include_router(utils.router, prefix="/utils", tags=["utils"])


app.include_router(device.router, prefix="/devices", tags=["devices"])
app.include_router(ip_log.router, prefix="/ip_logs", tags=["ip_logs"])
app.include_router(rewards.router, prefix="/rewards", tags=["rewards"])
app.include_router(reward_date.router, prefix="/rewarddate", tags=["reward_date"])
app.include_router(conversation.router, prefix="/conversation", tags=["conversation"])
app.include_router(third.router, prefix="/third", tags=["third"])
app.include_router(kycrestrict.router, prefix="/kyc", tags=["kyc"])
app.include_router(error_log.router, prefix="/errorlog", tags=["error_log"])

app.include_router(completion.router, prefix="/chat", tags=["aliqwen"])
app.include_router(mcphttp.router, prefix="/mcp", tags=["aliqwen"])

@app.get("/")
async def get_status():
    return {
        "status": True,
        "auth": WEBUI_AUTH,
        "default_models": app.state.config.DEFAULT_MODELS,
        "default_prompt_suggestions": app.state.config.DEFAULT_PROMPT_SUGGESTIONS,
    }
