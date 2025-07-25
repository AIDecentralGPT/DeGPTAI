#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit

echo "Current directory: $SCRIPT_DIR"

KEY_FILE=.webui_secret_key

PORT="${PORT:-8080}"
HOST="${HOST:-0.0.0.0}"
echo "PORT: $PORT"
echo "HOST: $HOST"

if test "$WEBUI_SECRET_KEY $WEBUI_JWT_SECRET_KEY" = " "; then
  echo "Loading WEBUI_SECRET_KEY from file, not provided as an environment variable."

  if ! [ -e "$KEY_FILE" ]; then
    echo "Generating WEBUI_SECRET_KEY"
    # Generate a random value to use as a WEBUI_SECRET_KEY in case the user didn't provide one.
    echo $(head -c 12 /dev/random | base64) > "$KEY_FILE"
  fi

  echo "Loading WEBUI_SECRET_KEY from $KEY_FILE"
  WEBUI_SECRET_KEY=$(cat "$KEY_FILE")
  echo "WEBUI_SECRET_KEY: $WEBUI_SECRET_KEY"
fi

if [ "$USE_OLLAMA_DOCKER" = "true" ]; then
    echo "USE_OLLAMA is set to true, starting ollama serve."
    ollama serve &
fi

if [ "$USE_CUDA_DOCKER" = "true" ]; then
  echo "CUDA is enabled, appending LD_LIBRARY_PATH to include torch/cudnn & cublas libraries."
  export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib/python3.11/site-packages/torch/lib:/usr/local/lib/python3.11/site-packages/nvidia/cudnn/lib"
  echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
fi

echo "Starting uvicorn..."
echo WEBUI_SECRET_KEY="$WEBUI_SECRET_KEY" uvicorn main:app --host "$HOST" --port "$PORT" --forwarded-allow-ips '*'
#  加上 --reload进行热更新
# WEBUI_SECRET_KEY="$WEBUI_SECRET_KEY" exec uvicorn main:app  --host "$HOST" --port "$PORT" --forwarded-allow-ips '*'
WEBUI_SECRET_KEY="$WEBUI_SECRET_KEY" exec uvicorn main:app \
    --workers 4 \
    --host "$HOST" \
    --port "$PORT" \
    --forwarded-allow-ips '*' \
    --timeout-keep-alive 65