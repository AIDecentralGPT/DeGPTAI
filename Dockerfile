# syntax=docker/dockerfile:1
# Initialize device type args
# use build args in the docker build commmand with --build-arg="BUILDARG=true"
ARG USE_CUDA=false
ARG USE_OLLAMA=false
# Tested with cu117 for CUDA 11 and cu121 for CUDA 12 (default)
ARG USE_CUDA_VER=cu121
# any sentence transformer model; models to use can be found at https://huggingface.co/models?library=sentence-transformers
# Leaderboard: https://huggingface.co/spaces/mteb/leaderboard 
# for better performance and multilangauge support use "intfloat/multilingual-e5-large" (~2.5GB) or "intfloat/multilingual-e5-base" (~1.5GB)
# IMPORTANT: If you change the embedding model (sentence-transformers/all-MiniLM-L6-v2) and vice versa, you aren't able to use RAG Chat with your previous documents loaded in the WebUI! You need to re-embed them.
ARG USE_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
ARG USE_RERANKING_MODEL=""
# Override at your own risk - non-root configurations are untested
ARG UID=0
ARG GID=0

######## WebUI frontend ########
FROM --platform=$BUILDPLATFORM node:21-alpine3.19 as build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build


<<<<<<< HEAD
# Delete the node_modules directory to reduce the image size.
RUN rm -rf node_modules
# Clean up the temporary files generated during the build process.
=======
# 删除node_modules以减小镜像体积
RUN rm -rf node_modules
# 清理构建中生成的临时文件
>>>>>>> fingerprintAuth-out
RUN rm -rf /app/src /app/public /app/tests /app/*.js 

######## WebUI backend ########
FROM python:3.11-slim-bookworm as base

# Use args
ARG USE_CUDA
ARG USE_OLLAMA
ARG USE_CUDA_VER
ARG USE_EMBEDDING_MODEL
ARG USE_RERANKING_MODEL
ARG UID
ARG GID

## Basis ##
ENV ENV=prod \
    PORT=8080 \
    # pass build args to the build
    USE_OLLAMA_DOCKER=${USE_OLLAMA} \
    USE_CUDA_DOCKER=${USE_CUDA} \
    USE_CUDA_DOCKER_VER=${USE_CUDA_VER} \
    USE_EMBEDDING_MODEL_DOCKER=${USE_EMBEDDING_MODEL} \
    USE_RERANKING_MODEL_DOCKER=${USE_RERANKING_MODEL}

## Basis URL Config ##
ENV OLLAMA_BASE_URL="/ollama" \
    OPENAI_API_BASE_URL=""

## API Key and Security Config ##
ENV OPENAI_API_KEY="" \
    WEBUI_SECRET_KEY="" \
    SCARF_NO_ANALYTICS=true \
    DO_NOT_TRACK=true \
    ANONYMIZED_TELEMETRY=false

# Use locally bundled version of the LiteLLM cost map json
# to avoid repetitive startup connections
ENV LITELLM_LOCAL_MODEL_COST_MAP="True"


#### Other models #########################################################
## whisper TTS model settings ##
ENV WHISPER_MODEL="base" \
    WHISPER_MODEL_DIR="/app/backend/data/cache/whisper/models"

## RAG Embedding model settings ##
ENV RAG_EMBEDDING_MODEL="$USE_EMBEDDING_MODEL_DOCKER" \
    RAG_RERANKING_MODEL="$USE_RERANKING_MODEL_DOCKER" \
    SENTENCE_TRANSFORMERS_HOME="/app/backend/data/cache/embedding/models"

## Hugging Face download cache ##
ENV HF_HOME="/app/backend/data/cache/embedding/models"
#### Other models ##########################################################

WORKDIR /app/backend

ENV HOME /root
# Create user and group if not root
RUN if [ $UID -ne 0 ]; then \
      if [ $GID -ne 0 ]; then \
        addgroup --gid $GID app; \
      fi; \
      adduser --uid $UID --gid $GID --home $HOME --disabled-password --no-create-home app; \
    fi

RUN mkdir -p $HOME/.cache/chroma
RUN echo -n 00000000-0000-0000-0000-000000000000 > $HOME/.cache/chroma/telemetry_user_id

# Make sure the user has access to the app and root directory
RUN chown -R $UID:$GID /app $HOME

RUN if [ "$USE_OLLAMA" = "true" ]; then \
    apt-get update && \
    # Install pandoc and netcat
    apt-get install -y --no-install-recommends pandoc netcat-openbsd curl && \
    # for RAG OCR
    apt-get install -y --no-install-recommends ffmpeg libsm6 libxext6 && \
    # install helper tools
    apt-get install -y --no-install-recommends curl jq && \
    # install ollama
    curl -fsSL https://ollama.com/install.sh | sh && \
    # cleanup
    rm -rf /var/lib/apt/lists/*; \
    else \
    apt-get update && \
    # Install pandoc and netcat
    apt-get install -y --no-install-recommends pandoc netcat-openbsd curl jq && \
    # for RAG OCR
    apt-get install -y --no-install-recommends ffmpeg libsm6 libxext6 && \
    # cleanup
    rm -rf /var/lib/apt/lists/*; \
    fi

# install python dependencies
COPY --chown=$UID:$GID ./backend/requirements.txt ./requirements.txt

# RUN pip3 install uv && \
#     if [ "$USE_CUDA" = "true" ]; then \
#     # If you use CUDA the whisper and embedding model will be downloaded on first use
#     pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/$USE_CUDA_DOCKER_VER --no-cache-dir && \
#     uv pip install --system -r requirements.txt --no-cache-dir && \
#     python -c "import os; from sentence_transformers import SentenceTransformer; SentenceTransformer(os.environ['RAG_EMBEDDING_MODEL'], device='cpu')" && \
#     python -c "import os; from faster_whisper import WhisperModel; WhisperModel(os.environ['WHISPER_MODEL'], device='cpu', compute_type='int8', download_root=os.environ['WHISPER_MODEL_DIR'])"; \
#     else \
#     pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --no-cache-dir && \
#     uv pip install --system -r requirements.txt --no-cache-dir && \
#     python -c "import os; from sentence_transformers import SentenceTransformer; SentenceTransformer(os.environ['RAG_EMBEDDING_MODEL'], device='cpu')" && \
#     python -c "import os; from faster_whisper import WhisperModel; WhisperModel(os.environ['WHISPER_MODEL'], device='cpu', compute_type='int8', download_root=os.environ['WHISPER_MODEL_DIR'])"; \
#     fi

<<<<<<< HEAD
# Download and install CUDA-related dependencies.
=======
# 下载和安装 CUDA 相关依赖
>>>>>>> fingerprintAuth-out
RUN pip3 install uv && \
    if [ "$USE_CUDA" = "true" ]; then \
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/$USE_CUDA_DOCKER_VER --no-cache-dir; \
    else \
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --no-cache-dir; \
    fi

<<<<<<< HEAD
# Install Python dependencies
COPY --chown=$UID:$GID ./backend/requirements.txt ./requirements.txt
RUN uv pip install --system -r requirements.txt --no-cache-dir

# Download Hugging Face models
RUN python -c "import os; from sentence_transformers import SentenceTransformer; SentenceTransformer(os.environ['RAG_EMBEDDING_MODEL'], device='cpu')" && \
    python -c "import os; from faster_whisper import WhisperModel; WhisperModel(os.environ['WHISPER_MODEL'], device='cpu', compute_type='int8', download_root=os.environ['WHISPER_MODEL_DIR'])"



=======
# 安装 Python 依赖
COPY --chown=$UID:$GID ./backend/requirements.txt ./requirements.txt
RUN uv pip install --system -r requirements.txt --no-cache-dir

# 安装 playwright 环境
RUN apt-get update && \
    apt-get install -y binutils && \
    apt-get install -y \
    wget \
    curl \
    # --- 核心浏览器依赖 ---
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    # --- GTK 和图形支持 ---
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    # --- 多媒体支持（GStreamer） ---
    gstreamer1.0-libav \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    # --- 其他关键库 ---
    libatomic1 \
    libxslt1.1 \
    libharfbuzz-icu0 \
    libenchant-2-2 \
    libsecret-1-0 \
    libhyphen0 \
    libmanette-0.2-0 \
    libgles2-mesa \
    # --- 中文字体支持 ---
    fonts-noto \
    fonts-noto-cjk \
    fonts-wqy-microhei \
    fonts-wqy-zenhei \
    # 清理缓存以减小镜像体积
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 下载playwright网页浏览器
Run playwright install

# 下载 Hugging Face 模型
RUN python -c "import os; from sentence_transformers import SentenceTransformer; SentenceTransformer(os.environ['RAG_EMBEDDING_MODEL'], device='cpu')" && \
    python -c "import os; from faster_whisper import WhisperModel; WhisperModel(os.environ['WHISPER_MODEL'], device='cpu', compute_type='int8', download_root=os.environ['WHISPER_MODEL_DIR'])"

>>>>>>> fingerprintAuth-out
# copy embedding weight from build
# RUN mkdir -p /root/.cache/chroma/onnx_models/all-MiniLM-L6-v2
# COPY --from=build /app/onnx /root/.cache/chroma/onnx_models/all-MiniLM-L6-v2/onnx

# copy built frontend files
COPY --chown=$UID:$GID --from=build /app/build /app/build
COPY --chown=$UID:$GID --from=build /app/CHANGELOG.md /app/CHANGELOG.md
COPY --chown=$UID:$GID --from=build /app/package.json /app/package.json

# copy backend files
COPY --chown=$UID:$GID ./backend .

EXPOSE 8080

HEALTHCHECK CMD curl --silent --fail http://localhost:8080/health | jq -e '.status == true' || exit 1

USER $UID:$GID

<<<<<<< HEAD
# Time zone setting
=======
# 时区设置
>>>>>>> fingerprintAuth-out
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD [ "bash", "start.sh"]


# ARG USE_CUDA=false
# ARG USE_OLLAMA=false
<<<<<<< HEAD
# # Whether to use CUDA and OLLAMA, with the default value being false.


# ARG USE_CUDA_VER=cu121
# # CUDA version, the default is cu121.
=======
# # 是否使用CUDA和OLLAMA，默认为false


# ARG USE_CUDA_VER=cu121
# # CUDA版本，默认是cu121
>>>>>>> fingerprintAuth-out





# ARG USE_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
# ARG USE_RERANKING_MODEL=""
<<<<<<< HEAD
# # Specify the embedding model and the re-ranking model to be used.
=======
# # 指定使用的嵌入模型和重新排序模型
>>>>>>> fingerprintAuth-out


# ARG UID=0
# ARG GID=0
<<<<<<< HEAD
# # User and group IDs, with the default being 0 (root).
=======
# # 用户和组的ID，默认是0（root）
>>>>>>> fingerprintAuth-out

# ######## WebUI frontend ########
# FROM --platform=$BUILDPLATFORM node:21-alpine3.19 as build

# WORKDIR /app

# COPY package.json package-lock.json ./
# RUN npm ci
<<<<<<< HEAD
# # Install Node.js dependencies.

# COPY . .
# RUN npm run build
# # Build the front end

# # Delete the node_modules directory to reduce the image size
# RUN rm -rf node_modules
# # Clean up the temporary files generated during the build process
=======
# # 安装Node.js依赖

# COPY . .
# RUN npm run build
# # 构建前端

# # 删除node_modules以减小镜像体积
# RUN rm -rf node_modules
# # 清理构建中生成的临时文件
>>>>>>> fingerprintAuth-out
# RUN rm -rf /app/src /app/public /app/tests /app/*.js 








<<<<<<< HEAD
# ######## backend ########
=======
# ######## 后端 ########
>>>>>>> fingerprintAuth-out
# FROM python:3.11-slim-bookworm as base

# # Use args
# ARG USE_CUDA
# ARG USE_OLLAMA
# ARG USE_CUDA_VER
# ARG USE_EMBEDDING_MODEL
# ARG USE_RERANKING_MODEL
# ARG UID
# ARG GID
<<<<<<< HEAD
# # Use the parameters defined above
=======
# # 使用上述定义的参数
>>>>>>> fingerprintAuth-out

# ## Basis ##
# ENV ENV=prod \
#     PORT=8080 \
#     USE_OLLAMA_DOCKER=${USE_OLLAMA} \
#     USE_CUDA_DOCKER=${USE_CUDA} \
#     USE_CUDA_DOCKER_VER=${USE_CUDA_VER} \
#     USE_EMBEDDING_MODEL_DOCKER=${USE_EMBEDDING_MODEL} \
#     USE_RERANKING_MODEL_DOCKER=${USE_RERANKING_MODEL}
<<<<<<< HEAD
# # Set environment variables
=======
# # 设置环境变量
>>>>>>> fingerprintAuth-out

# ## Basis URL Config ##
# ENV OLLAMA_BASE_URL="/ollama" \
#     OPENAI_API_BASE_URL=""
<<<<<<< HEAD
# # URL configuration
=======
# # URL配置
>>>>>>> fingerprintAuth-out

# ## API Key and Security Config ##
# ENV OPENAI_API_KEY="" \
#     WEBUI_SECRET_KEY="" \
#     SCARF_NO_ANALYTICS=true \
#     DO_NOT_TRACK=true \
#     ANONYMIZED_TELEMETRY=false
<<<<<<< HEAD
# # API key and security configuration

# # Use locally bundled version of the LiteLLM cost map json
# # Use the local LiteLLM cost map JSON
=======
# # API密钥和安全配置

# # Use locally bundled version of the LiteLLM cost map json
# # 使用本地的LiteLLM成本地图JSON
>>>>>>> fingerprintAuth-out

# ENV LITELLM_LOCAL_MODEL_COST_MAP="True"

# #### Other models #########################################################
# ## whisper TTS model settings ##
# ENV WHISPER_MODEL="base" \
#     WHISPER_MODEL_DIR="/app/backend/data/cache/whisper/models"
<<<<<<< HEAD
# # Whisper TTS model configuration
=======
# # Whisper TTS模型配置
>>>>>>> fingerprintAuth-out

# ## RAG Embedding model settings ##
# ENV RAG_EMBEDDING_MODEL="$USE_EMBEDDING_MODEL_DOCKER" \
#     RAG_RERANKING_MODEL="$USE_RERANKING_MODEL_DOCKER" \
#     SENTENCE_TRANSFORMERS_HOME="/app/backend/data/cache/embedding/models"
<<<<<<< HEAD
# # RAG embedding model configuration

# ## Hugging Face download cache ##
# ENV HF_HOME="/app/backend/data/cache/embedding/models"
# # Hugging Face download cache configuration
=======
# # RAG嵌入模型配置

# ## Hugging Face download cache ##
# ENV HF_HOME="/app/backend/data/cache/embedding/models"
# # Hugging Face下载缓存配置
>>>>>>> fingerprintAuth-out

# #### Other models ##########################################################





# WORKDIR /app/backend

# ENV HOME /root
<<<<<<< HEAD
# # Create a user and a group if not the root user
=======
# # 创建用户和组，如果不是root
>>>>>>> fingerprintAuth-out
# RUN if [ $UID -ne 0 ]; then \
#       if [ $GID -ne 0 ]; then \
#         addgroup --gid $GID app; \
#       fi; \
#       adduser --uid $UID --gid $GID --home $HOME --disabled-password --no-create-home app; \
#     fi

# RUN mkdir -p $HOME/.cache/chroma
# RUN echo -n 00000000-0000-0000-0000-000000000000 > $HOME/.cache/chroma/telemetry_user_id

<<<<<<< HEAD
# # Ensure that the user has access rights to the application and the root directory
=======
# # 确保用户对应用程序和根目录有访问权限
>>>>>>> fingerprintAuth-out
# RUN chown -R $UID:$GID /app $HOME

# RUN apt-get update && \
#     # Install pandoc and netcat
#     apt-get install -y --no-install-recommends pandoc netcat-openbsd curl jq && \
#     # for RAG OCR
#     apt-get install -y --no-install-recommends ffmpeg libsm6 libxext6 && \
#     # cleanup
#     rm -rf /var/lib/apt/lists/*; 
<<<<<<< HEAD
# # Install the corresponding dependencies according to the value of USE_OLLAMA



# # Install Python dependencies
=======
# # 根据USE_OLLAMA的值安装相应的依赖



# # 安装Python依赖
>>>>>>> fingerprintAuth-out
# COPY --chown=$UID:$GID ./backend/requirements.txt ./requirements.txt
# RUN pip3 install uv
# RUN uv pip install --system -r requirements.txt --no-cache-dir

<<<<<<< HEAD
# # Copy the built front-end files
=======
# # 复制构建的前端文件
>>>>>>> fingerprintAuth-out
# COPY --chown=$UID:$GID --from=build /app/build /app/build
# COPY --chown=$UID:$GID --from=build /app/CHANGELOG.md /app/CHANGELOG.md
# COPY --chown=$UID:$GID --from=build /app/package.json /app/package.json

<<<<<<< HEAD
# # Copy the back-end files
=======
# # 复制后端文件
>>>>>>> fingerprintAuth-out
# COPY --chown=$UID:$GID ./backend .

# EXPOSE 8080

# HEALTHCHECK CMD curl --silent --fail http://localhost:8080/health | jq -e '.status == true' || exit 1

# USER $UID:$GID

# CMD [ "bash", "start.sh"]
<<<<<<< HEAD
# # Set the startup command
=======
# # 设置启动命令
>>>>>>> fingerprintAuth-out
