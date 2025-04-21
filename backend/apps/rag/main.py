from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form,
)
from fastapi.middleware.cors import CORSMiddleware
import os, shutil, logging, re

from pathlib import Path
from typing import List

from chromadb.utils.batch_utils import create_batches

from langchain_community.document_loaders import (
    WebBaseLoader,
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    BSHTMLLoader,
    Docx2txtLoader,
    UnstructuredEPubLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader,
    UnstructuredXMLLoader,
    UnstructuredRSTLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader,
    YoutubeLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 导入 unstructured 库中涉及分词的模块
import unstructured.nlp.tokenize

import validators
import urllib.parse
import socket
import zipfile
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from apps.rag.oss import OSSUtil
from apps.rag.pptimage import PPTIMAGEUTIL

from pydantic import BaseModel
from typing import Optional
import mimetypes
import uuid
import json
import fitz

import sentence_transformers

from apps.web.models.documents import (
    Documents,
    DocumentForm,
    DocumentResponse,
)

from apps.rag.utils import (
    get_model_path,
    get_embedding_function,
    query_doc,
    query_doc_with_hybrid_search,
    query_collection,
    query_collection_with_hybrid_search,
)

from utils.misc import (
    calculate_sha256,
    calculate_sha256_string,
    sanitize_filename,
    extract_folders_after_data_docs,
)
from utils.utils import get_current_user, get_admin_user

from config import (
    ENV,
    SRC_LOG_LEVELS,
    UPLOAD_DIR,
    DOCS_DIR,
    RAG_TOP_K,
    RAG_RELEVANCE_THRESHOLD,
    RAG_EMBEDDING_ENGINE,
    RAG_EMBEDDING_MODEL,
    RAG_EMBEDDING_MODEL_AUTO_UPDATE,
    RAG_EMBEDDING_MODEL_TRUST_REMOTE_CODE,
    ENABLE_RAG_HYBRID_SEARCH,
    ENABLE_RAG_WEB_LOADER_SSL_VERIFICATION,
    RAG_RERANKING_MODEL,
    PDF_EXTRACT_IMAGES,
    RAG_RERANKING_MODEL_AUTO_UPDATE,
    RAG_RERANKING_MODEL_TRUST_REMOTE_CODE,
    RAG_OPENAI_API_BASE_URL,
    RAG_OPENAI_API_KEY,
    DEVICE_TYPE,
    CHROMA_CLIENT,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    RAG_TEMPLATE,
    ENABLE_RAG_LOCAL_WEB_FETCH,
    YOUTUBE_LOADER_LANGUAGE,
    AppConfig,
)

from constants import ERROR_MESSAGES

import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
#print("====================", nltk.data.path)


log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])

app = FastAPI()

app.state.config = AppConfig()

app.state.config.TOP_K = RAG_TOP_K
app.state.config.RELEVANCE_THRESHOLD = RAG_RELEVANCE_THRESHOLD

app.state.config.ENABLE_RAG_HYBRID_SEARCH = ENABLE_RAG_HYBRID_SEARCH
app.state.config.ENABLE_RAG_WEB_LOADER_SSL_VERIFICATION = (
    ENABLE_RAG_WEB_LOADER_SSL_VERIFICATION
)

app.state.config.CHUNK_SIZE = CHUNK_SIZE
app.state.config.CHUNK_OVERLAP = CHUNK_OVERLAP

app.state.config.RAG_EMBEDDING_ENGINE = RAG_EMBEDDING_ENGINE
app.state.config.RAG_EMBEDDING_MODEL = RAG_EMBEDDING_MODEL
app.state.config.RAG_RERANKING_MODEL = RAG_RERANKING_MODEL
app.state.config.RAG_TEMPLATE = RAG_TEMPLATE


app.state.config.OPENAI_API_BASE_URL = RAG_OPENAI_API_BASE_URL
app.state.config.OPENAI_API_KEY = RAG_OPENAI_API_KEY

app.state.config.PDF_EXTRACT_IMAGES = PDF_EXTRACT_IMAGES


app.state.config.YOUTUBE_LOADER_LANGUAGE = YOUTUBE_LOADER_LANGUAGE
app.state.YOUTUBE_LOADER_TRANSLATION = None


def update_embedding_model(
    embedding_model: str,
    update_model: bool = False,
):
    if embedding_model and app.state.config.RAG_EMBEDDING_ENGINE == "":
        app.state.sentence_transformer_ef = sentence_transformers.SentenceTransformer(
            get_model_path(embedding_model, update_model),
            device=DEVICE_TYPE,
            trust_remote_code=RAG_EMBEDDING_MODEL_TRUST_REMOTE_CODE,
        )
    else:
        app.state.sentence_transformer_ef = None


def update_reranking_model(
    reranking_model: str,
    update_model: bool = False,
):
    if reranking_model:
        app.state.sentence_transformer_rf = sentence_transformers.CrossEncoder(
            get_model_path(reranking_model, update_model),
            device=DEVICE_TYPE,
            trust_remote_code=RAG_RERANKING_MODEL_TRUST_REMOTE_CODE,
        )
    else:
        app.state.sentence_transformer_rf = None


update_embedding_model(
    app.state.config.RAG_EMBEDDING_MODEL,
    RAG_EMBEDDING_MODEL_AUTO_UPDATE,
)

update_reranking_model(
    app.state.config.RAG_RERANKING_MODEL,
    RAG_RERANKING_MODEL_AUTO_UPDATE,
)


app.state.EMBEDDING_FUNCTION = get_embedding_function(
    app.state.config.RAG_EMBEDDING_ENGINE,
    app.state.config.RAG_EMBEDDING_MODEL,
    app.state.sentence_transformer_ef,
    app.state.config.OPENAI_API_KEY,
    app.state.config.OPENAI_API_BASE_URL,
)

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CollectionNameForm(BaseModel):
    collection_name: Optional[str] = "test"


class UrlForm(CollectionNameForm):
    url: str


@app.get("/")
async def get_status():
    return {
        "status": True,
        "chunk_size": app.state.config.CHUNK_SIZE,
        "chunk_overlap": app.state.config.CHUNK_OVERLAP,
        "template": app.state.config.RAG_TEMPLATE,
        "embedding_engine": app.state.config.RAG_EMBEDDING_ENGINE,
        "embedding_model": app.state.config.RAG_EMBEDDING_MODEL,
        "reranking_model": app.state.config.RAG_RERANKING_MODEL,
    }


@app.get("/embedding")
async def get_embedding_config(user=Depends(get_admin_user)):
    return {
        "status": True,
        "embedding_engine": app.state.config.RAG_EMBEDDING_ENGINE,
        "embedding_model": app.state.config.RAG_EMBEDDING_MODEL,
        "openai_config": {
            "url": app.state.config.OPENAI_API_BASE_URL,
            "key": app.state.config.OPENAI_API_KEY,
        },
    }


@app.get("/reranking")
async def get_reraanking_config(user=Depends(get_admin_user)):
    return {
        "status": True,
        "reranking_model": app.state.config.RAG_RERANKING_MODEL,
    }


class OpenAIConfigForm(BaseModel):
    url: str
    key: str


class EmbeddingModelUpdateForm(BaseModel):
    openai_config: Optional[OpenAIConfigForm] = None
    embedding_engine: str
    embedding_model: str


@app.post("/embedding/update")
async def update_embedding_config(
    form_data: EmbeddingModelUpdateForm, user=Depends(get_admin_user)
):
    log.info(
        f"Updating embedding model: {app.state.config.RAG_EMBEDDING_MODEL} to {form_data.embedding_model}"
    )
    try:
        app.state.config.RAG_EMBEDDING_ENGINE = form_data.embedding_engine
        app.state.config.RAG_EMBEDDING_MODEL = form_data.embedding_model

        if app.state.config.RAG_EMBEDDING_ENGINE in ["ollama", "openai"]:
            if form_data.openai_config != None:
                app.state.config.OPENAI_API_BASE_URL = form_data.openai_config.url
                app.state.config.OPENAI_API_KEY = form_data.openai_config.key

        update_embedding_model(app.state.config.RAG_EMBEDDING_MODEL)

        app.state.EMBEDDING_FUNCTION = get_embedding_function(
            app.state.config.RAG_EMBEDDING_ENGINE,
            app.state.config.RAG_EMBEDDING_MODEL,
            app.state.sentence_transformer_ef,
            app.state.config.OPENAI_API_KEY,
            app.state.config.OPENAI_API_BASE_URL,
        )

        return {
            "status": True,
            "embedding_engine": app.state.config.RAG_EMBEDDING_ENGINE,
            "embedding_model": app.state.config.RAG_EMBEDDING_MODEL,
            "openai_config": {
                "url": app.state.config.OPENAI_API_BASE_URL,
                "key": app.state.config.OPENAI_API_KEY,
            },
        }
    except Exception as e:
        log.exception(f"Problem updating embedding model: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )


class RerankingModelUpdateForm(BaseModel):
    reranking_model: str


@app.post("/reranking/update")
async def update_reranking_config(
    form_data: RerankingModelUpdateForm, user=Depends(get_admin_user)
):
    log.info(
        f"Updating reranking model: {app.state.config.RAG_RERANKING_MODEL} to {form_data.reranking_model}"
    )
    try:
        app.state.config.RAG_RERANKING_MODEL = form_data.reranking_model

        update_reranking_model(app.state.config.RAG_RERANKING_MODEL), True

        return {
            "status": True,
            "reranking_model": app.state.config.RAG_RERANKING_MODEL,
        }
    except Exception as e:
        log.exception(f"Problem updating reranking model: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )


@app.get("/config")
async def get_rag_config(user=Depends(get_admin_user)):
    return {
        "status": True,
        "pdf_extract_images": app.state.config.PDF_EXTRACT_IMAGES,
        "chunk": {
            "chunk_size": app.state.config.CHUNK_SIZE,
            "chunk_overlap": app.state.config.CHUNK_OVERLAP,
        },
        "web_loader_ssl_verification": app.state.config.ENABLE_RAG_WEB_LOADER_SSL_VERIFICATION,
        "youtube": {
            "language": app.state.config.YOUTUBE_LOADER_LANGUAGE,
            "translation": app.state.YOUTUBE_LOADER_TRANSLATION,
        },
    }


class ChunkParamUpdateForm(BaseModel):
    chunk_size: int
    chunk_overlap: int


class YoutubeLoaderConfig(BaseModel):
    language: List[str]
    translation: Optional[str] = None


class ConfigUpdateForm(BaseModel):
    pdf_extract_images: Optional[bool] = None
    chunk: Optional[ChunkParamUpdateForm] = None
    web_loader_ssl_verification: Optional[bool] = None
    youtube: Optional[YoutubeLoaderConfig] = None


@app.post("/config/update")
async def update_rag_config(form_data: ConfigUpdateForm, user=Depends(get_admin_user)):
    app.state.config.PDF_EXTRACT_IMAGES = (
        form_data.pdf_extract_images
        if form_data.pdf_extract_images is not None
        else app.state.config.PDF_EXTRACT_IMAGES
    )

    app.state.config.CHUNK_SIZE = (
        form_data.chunk.chunk_size
        if form_data.chunk is not None
        else app.state.config.CHUNK_SIZE
    )

    app.state.config.CHUNK_OVERLAP = (
        form_data.chunk.chunk_overlap
        if form_data.chunk is not None
        else app.state.config.CHUNK_OVERLAP
    )

    app.state.config.ENABLE_RAG_WEB_LOADER_SSL_VERIFICATION = (
        form_data.web_loader_ssl_verification
        if form_data.web_loader_ssl_verification != None
        else app.state.config.ENABLE_RAG_WEB_LOADER_SSL_VERIFICATION
    )

    app.state.config.YOUTUBE_LOADER_LANGUAGE = (
        form_data.youtube.language
        if form_data.youtube is not None
        else app.state.config.YOUTUBE_LOADER_LANGUAGE
    )

    app.state.YOUTUBE_LOADER_TRANSLATION = (
        form_data.youtube.translation
        if form_data.youtube is not None
        else app.state.YOUTUBE_LOADER_TRANSLATION
    )

    return {
        "status": True,
        "pdf_extract_images": app.state.config.PDF_EXTRACT_IMAGES,
        "chunk": {
            "chunk_size": app.state.config.CHUNK_SIZE,
            "chunk_overlap": app.state.config.CHUNK_OVERLAP,
        },
        "web_loader_ssl_verification": app.state.config.ENABLE_RAG_WEB_LOADER_SSL_VERIFICATION,
        "youtube": {
            "language": app.state.config.YOUTUBE_LOADER_LANGUAGE,
            "translation": app.state.YOUTUBE_LOADER_TRANSLATION,
        },
    }


@app.get("/template")
async def get_rag_template(user=Depends(get_current_user)):
    return {
        "status": True,
        "template": app.state.config.RAG_TEMPLATE,
    }


@app.get("/query/settings")
async def get_query_settings(user=Depends(get_admin_user)):
    return {
        "status": True,
        "template": app.state.config.RAG_TEMPLATE,
        "k": app.state.config.TOP_K,
        "r": app.state.config.RELEVANCE_THRESHOLD,
        "hybrid": app.state.config.ENABLE_RAG_HYBRID_SEARCH,
    }


class QuerySettingsForm(BaseModel):
    k: Optional[int] = None
    r: Optional[float] = None
    template: Optional[str] = None
    hybrid: Optional[bool] = None


@app.post("/query/settings/update")
async def update_query_settings(
    form_data: QuerySettingsForm, user=Depends(get_admin_user)
):
    app.state.config.RAG_TEMPLATE = (
        form_data.template if form_data.template else RAG_TEMPLATE
    )
    app.state.config.TOP_K = form_data.k if form_data.k else 4
    app.state.config.RELEVANCE_THRESHOLD = form_data.r if form_data.r else 0.0
    app.state.config.ENABLE_RAG_HYBRID_SEARCH = (
        form_data.hybrid if form_data.hybrid else False
    )
    return {
        "status": True,
        "template": app.state.config.RAG_TEMPLATE,
        "k": app.state.config.TOP_K,
        "r": app.state.config.RELEVANCE_THRESHOLD,
        "hybrid": app.state.config.ENABLE_RAG_HYBRID_SEARCH,
    }


class QueryDocForm(BaseModel):
    collection_name: str
    query: str
    k: Optional[int] = None
    r: Optional[float] = None
    hybrid: Optional[bool] = None


@app.post("/query/doc")
def query_doc_handler(
    form_data: QueryDocForm,
    user=Depends(get_current_user),
):
    try:
        if app.state.config.ENABLE_RAG_HYBRID_SEARCH:
            return query_doc_with_hybrid_search(
                collection_name=form_data.collection_name,
                query=form_data.query,
                embedding_function=app.state.EMBEDDING_FUNCTION,
                k=form_data.k if form_data.k else app.state.config.TOP_K,
                reranking_function=app.state.sentence_transformer_rf,
                r=(
                    form_data.r if form_data.r else app.state.config.RELEVANCE_THRESHOLD
                ),
            )
        else:
            return query_doc(
                collection_name=form_data.collection_name,
                query=form_data.query,
                embedding_function=app.state.EMBEDDING_FUNCTION,
                k=form_data.k if form_data.k else app.state.config.TOP_K,
            )
    except Exception as e:
        log.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )


class QueryCollectionsForm(BaseModel):
    collection_names: List[str]
    query: str
    k: Optional[int] = None
    r: Optional[float] = None
    hybrid: Optional[bool] = None


@app.post("/query/collection")
def query_collection_handler(
    form_data: QueryCollectionsForm,
    user=Depends(get_current_user),
):
    try:
        if app.state.config.ENABLE_RAG_HYBRID_SEARCH:
            return query_collection_with_hybrid_search(
                collection_names=form_data.collection_names,
                query=form_data.query,
                embedding_function=app.state.EMBEDDING_FUNCTION,
                k=form_data.k if form_data.k else app.state.config.TOP_K,
                reranking_function=app.state.sentence_transformer_rf,
                r=(
                    form_data.r if form_data.r else app.state.config.RELEVANCE_THRESHOLD
                ),
            )
        else:
            return query_collection(
                collection_names=form_data.collection_names,
                query=form_data.query,
                embedding_function=app.state.EMBEDDING_FUNCTION,
                k=form_data.k if form_data.k else app.state.config.TOP_K,
            )

    except Exception as e:
        log.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )


@app.post("/youtube")
def store_youtube_video(form_data: UrlForm, user=Depends(get_current_user)):
    try:
        loader = YoutubeLoader.from_youtube_url(
            form_data.url,
            add_video_info=True,
            language=app.state.config.YOUTUBE_LOADER_LANGUAGE,
            translation=app.state.YOUTUBE_LOADER_TRANSLATION,
        )
        data = loader.load()

        collection_name = form_data.collection_name
        if collection_name == "":
            collection_name = calculate_sha256_string(form_data.url)[:63]

        store_data_in_vector_db(data, collection_name, overwrite=True)
        return {
            "status": True,
            "collection_name": collection_name,
            "filename": form_data.url,
        }
    except Exception as e:
        log.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )


@app.post("/web")
def store_web(form_data: UrlForm, user=Depends(get_current_user)):
    # "https://www.gutenberg.org/files/1727/1727-h/1727-h.htm"
    try:
        loader = get_web_loader(
            form_data.url,
            verify_ssl=app.state.config.ENABLE_RAG_WEB_LOADER_SSL_VERIFICATION,
        )
        data = loader.load()

        collection_name = form_data.collection_name
        if collection_name == "":
            collection_name = calculate_sha256_string(form_data.url)[:63]

        store_data_in_vector_db(data, collection_name, overwrite=True)
        return {
            "status": True,
            "collection_name": collection_name,
            "filename": form_data.url,
        }
    except Exception as e:
        log.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )


def get_web_loader(url: str, verify_ssl: bool = True):
    # Check if the URL is valid
    if isinstance(validators.url(url), validators.ValidationError):
        raise ValueError(ERROR_MESSAGES.INVALID_URL)
    if not ENABLE_RAG_LOCAL_WEB_FETCH:
        # Local web fetch is disabled, filter out any URLs that resolve to private IP addresses
        parsed_url = urllib.parse.urlparse(url)
        # Get IPv4 and IPv6 addresses
        ipv4_addresses, ipv6_addresses = resolve_hostname(parsed_url.hostname)
        # Check if any of the resolved addresses are private
        # This is technically still vulnerable to DNS rebinding attacks, as we don't control WebBaseLoader
        for ip in ipv4_addresses:
            if validators.ipv4(ip, private=True):
                raise ValueError(ERROR_MESSAGES.INVALID_URL)
        for ip in ipv6_addresses:
            if validators.ipv6(ip, private=True):
                raise ValueError(ERROR_MESSAGES.INVALID_URL)
    return WebBaseLoader(url, verify_ssl=verify_ssl)


def resolve_hostname(hostname):
    # Get address information
    addr_info = socket.getaddrinfo(hostname, None)

    # Extract IP addresses from address information
    ipv4_addresses = [info[4][0] for info in addr_info if info[0] == socket.AF_INET]
    ipv6_addresses = [info[4][0] for info in addr_info if info[0] == socket.AF_INET6]

    return ipv4_addresses, ipv6_addresses


def store_data_in_vector_db(data, collection_name, overwrite: bool = False) -> bool:

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=app.state.config.CHUNK_SIZE,
        chunk_overlap=app.state.config.CHUNK_OVERLAP,
        add_start_index=True,
    )

    docs = text_splitter.split_documents(data)

    if len(docs) > 0:
        log.info(f"store_data_in_vector_db {docs}")
        return store_docs_in_vector_db(docs, collection_name, overwrite), None
    else:
        raise ValueError(ERROR_MESSAGES.EMPTY_CONTENT)


def store_text_in_vector_db(
    text, metadata, collection_name, overwrite: bool = False
) -> bool:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=app.state.config.CHUNK_SIZE,
        chunk_overlap=app.state.config.CHUNK_OVERLAP,
        add_start_index=True,
    )
    docs = text_splitter.create_documents([text], metadatas=[metadata])
    return store_docs_in_vector_db(docs, collection_name, overwrite)


def store_docs_in_vector_db(docs, collection_name, overwrite: bool = False) -> bool:
    log.info(f"store_docs_in_vector_db {docs} {collection_name}")

    texts = [doc.page_content for doc in docs]
    metadatas = [doc.metadata for doc in docs]

    try:
        if overwrite:
            for collection in CHROMA_CLIENT.list_collections():
                if collection_name == collection.name:
                    log.info(f"deleting existing collection {collection_name}")
                    CHROMA_CLIENT.delete_collection(name=collection_name)

        collection = CHROMA_CLIENT.create_collection(name=collection_name)

        embedding_func = get_embedding_function(
            app.state.config.RAG_EMBEDDING_ENGINE,
            app.state.config.RAG_EMBEDDING_MODEL,
            app.state.sentence_transformer_ef,
            app.state.config.OPENAI_API_KEY,
            app.state.config.OPENAI_API_BASE_URL,
        )

        embedding_texts = list(map(lambda x: x.replace("\n", " "), texts))
        embeddings = embedding_func(embedding_texts)

        for batch in create_batches(
            api=CHROMA_CLIENT,
            ids=[str(uuid.uuid4()) for _ in texts],
            metadatas=metadatas,
            embeddings=embeddings,
            documents=texts,
        ):
            collection.add(*batch)

        return True
    except Exception as e:
        log.exception(e)
        if e.__class__.__name__ == "UniqueConstraintError":
            return True

        return False


# 定义一个空的分词函数，直接返回包含原文本的列表
def disable_tokenize(text):
    return [text]
# 将 unstructured 库中用于句子分词的函数替换为自定义的空分词函数
unstructured.nlp.tokenize._sent_tokenize = disable_tokenize

def get_loader(filename: str, file_content_type: str, file_path: str):
    file_ext = filename.split(".")[-1].lower()
    known_type = True

    known_source_ext = [
        "go",
        "py",
        "java",
        "sh",
        "bat",
        "ps1",
        "cmd",
        "js",
        "ts",
        "css",
        "cpp",
        "hpp",
        "h",
        "c",
        "cs",
        "sql",
        "log",
        "ini",
        "pl",
        "pm",
        "r",
        "dart",
        "dockerfile",
        "env",
        "php",
        "hs",
        "hsc",
        "lua",
        "nginxconf",
        "conf",
        "m",
        "mm",
        "plsql",
        "perl",
        "rb",
        "rs",
        "db2",
        "scala",
        "bash",
        "swift",
        "vue",
        "svelte",
    ]

    if file_ext == "pdf":
        loader = PyPDFLoader(
            file_path, extract_images=app.state.config.PDF_EXTRACT_IMAGES
        )
    elif file_ext == "csv":
        loader = CSVLoader(file_path, encoding="utf-8", 
                    csv_args={
                        "delimiter": ",",
                        "restval": ""
                    })
    elif file_ext == "rst":
        loader = UnstructuredRSTLoader(file_path, mode="elements")
    elif file_ext == "xml":
        loader = UnstructuredXMLLoader(file_path)
    elif file_ext in ["htm", "html"]:
        loader = BSHTMLLoader(file_path, open_encoding="unicode_escape")
    elif file_ext == "md":
        loader = UnstructuredMarkdownLoader(file_path)
    elif file_content_type == "application/epub+zip":
        loader = UnstructuredEPubLoader(file_path)
    elif (
        file_content_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        or file_ext in ["docx"]
    ):
        loader = UnstructuredWordDocumentLoader(file_path)
    elif file_content_type in [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ] or file_ext in ["xls", "xlsx"]:
        loader = UnstructuredExcelLoader(file_path)
    elif file_content_type in [
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ] or file_ext in ["ppt", "pptx"]:
        loader = UnstructuredPowerPointLoader(file_path)
    elif file_ext in known_source_ext or (
        file_content_type and file_content_type.find("text/") >= 0
    ):
        loader = TextLoader(file_path, autodetect_encoding=True)
    else:
        loader = TextLoader(file_path, autodetect_encoding=True)
        # known_type = False

    return loader, known_type

def get_images(filename: str, file_path: str):
    file_ext = filename.split(".")[-1].lower()
    images_base64 = []
    marge_base64 = None
    # 支持的图片扩展名及其对应的MIME类型
    image_mime_types = {
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'bmp': 'image/bmp',
        'webp': 'image/webp',
        'tiff': 'image/tiff',
    }

    if (file_ext in ["docx"]):
        # 以zip格式打开docx文件
        base64_images = []
        with zipfile.ZipFile(file_path, 'r') as docx:
            # 遍历zip内的所有文件
            for file_info in docx.infolist():
                # 检查文件是否在word/media目录下（图片存储位置）
                if file_info.filename.startswith('word/media/'):
                    # 读取图片二进制数据
                    image_data = docx.read(file_info)
                    
                    # 提取文件名和扩展名
                    filename = os.path.basename(file_info.filename)
                    file_ext = os.path.splitext(filename)[1].lower().strip('.')
                    
                    # 获取对应的MIME类型，默认使用'application/octet-stream'
                    mime_type = image_mime_types.get(file_ext, 'application/octet-stream')
                    
                    # 转换为Base64字符串
                    base64_str = base64.b64encode(image_data).decode('utf-8')
                    
                    # 组合成完整的数据URI
                    data_uri = f'data:{mime_type};base64,{base64_str}'

                    if verify_base64_image(data_uri):
                        print("============data_uri=============", data_uri)
                        base64_images.append(data_uri)
                    
            # 合并base64图片
            if len(base64_images) != 0:
                if len(base64_images) > 1:
                    marge_base64 = merge_base64_images(base64_images, 'vertical')
                else:
                    marge_base64 = base64_images[0]

    elif (file_ext in ["pdf"]):
        doc = fitz.open(file_path)
        base64_images = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)
        
            # 提取当前页所有图片
            for img_index, img_info in enumerate(image_list):
                xref = img_info[0]
                base_image = doc.extract_image(xref)
                image_data = base_image["image"]
            
                # 生成唯一文件名
                filename = f"page{page_num+1}_img{img_index+1}.{base_image['ext']}"
                file_ext = os.path.splitext(filename)[1].lower().strip('.')
            
                # 获取对应的MIME类型，默认使用'application/octet-stream'
                mime_type = image_mime_types.get(file_ext, 'application/octet-stream')   
                # 转换为Base64字符串
                base64_str = base64.b64encode(image_data).decode('utf-8')

                # 组合成完整的数据URI
                data_uri = f'data:{mime_type};base64,{base64_str}'

                if verify_base64_image(data_uri):
                    base64_images.append(data_uri)

            # 合并base64图片
            if len(base64_images) != 0:
                if len(base64_images) > 1:
                    marge_base64 = merge_base64_images(base64_images, 'vertical')
                else:
                    marge_base64 = base64_images[0]            
        doc.close()

    elif (file_ext in ["ppt", "pptx"]):
        base64_images = PPTIMAGEUTIL.extract_images(file_path)
        # 合并base64图片
        if len(base64_images) != 0:
            if len(base64_images) > 1:
                marge_base64 = merge_base64_images(base64_images, 'vertical')
            else:
                marge_base64 = base64_images[0]

    if marge_base64 is not None and verify_base64_image(marge_base64):
        result = OSSUtil.upload_base64_to_oss(marge_base64)
        if result is not None:
            images_base64.append(result)

    return images_base64

def merge_base64_images(base64_list, direction='horizontal', spacing=10, bg_color=(255, 255, 255)):
    try:
        # 将 Base64 转换为 PIL 图片对象列表
        images = []
        for b64 in base64_list:
            # 清理前缀 (如 data:image/png;base64)
            if "," in b64:
                b64 = b64.split(",", 1)[1]
            
            img_data = base64.b64decode(b64)
            img = Image.open(BytesIO(img_data)).convert("RGBA")
            images.append(img)

        # 统一尺寸 (取最小尺寸)
        if direction == 'horizontal':
            # 横向拼接：统一高度
            min_height = min(img.height for img in images)
            resized_images = [img.resize((int(img.width * min_height / img.height), min_height)) 
                              for img in images]
            widths = [img.width for img in resized_images]
            total_width = sum(widths) + spacing * (len(images) - 1)
            max_height = min_height
        else:
            # 纵向拼接：统一宽度
            # min_width = min(img.width for img in images)
            min_width = 600
            resized_images = [img.resize((min_width, int(img.height * min_width / img.width))) 
                              for img in images]
            heights = [img.height for img in resized_images]
            total_height = sum(heights) + spacing * (len(images) - 1)
            max_width = min_width

        # 创建画布
        if direction == 'horizontal':
            canvas = Image.new('RGB', (total_width, max_height), bg_color)
            x_offset = 0
            for img in resized_images:
                canvas.paste(img, (x_offset, 0), mask=img.split()[3] if img.mode == 'RGBA' else None)
                x_offset += img.width + spacing
        else:
            canvas = Image.new('RGB', (max_width, total_height), bg_color)
            y_offset = 0
            for img in resized_images:
                canvas.paste(img, (0, y_offset), mask=img.split()[3] if img.mode == 'RGBA' else None)
                y_offset += img.height + spacing

        # 转换为 Base64
        buffered = BytesIO()
        canvas.save(buffered, format="PNG")  # 可选 JPG
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # 添加前缀标识
        return f"data:image/png;base64,{img_base64}"
    
    except Exception as e:
        raise ValueError(f"图片合成失败: {str(e)}")

def verify_base64_image(base64_str):
    # 去除可能存在的前缀
    if base64_str.startswith('data:image'):
        # 找到逗号位置，截取逗号之后的部分
        comma_index = base64_str.find(',')
        if comma_index != -1:
            return True
    else:
        return False

# 压缩图片 
def compress_image_base64(base64_str, max_size_kb=10):
    # 去除前缀
    if base64_str.startswith('data:image'):
        comma_index = base64_str.find(',')
        if comma_index != -1:
            base64_str = base64_str[comma_index + 1:]

    # 将base64字符串解码为bytes
    img_data = base64.b64decode(base64_str)
    
    # 将bytes数据转换为Pillow Image对象
    img = Image.open(BytesIO(img_data))
    
    # 计算原始图片的字节大小
    original_size = len(img_data)
    print(f"Original size: {original_size} bytes")
    
    # 计算目标大小（100KB）的因子
    target_size = max_size_kb * 1024  # 将KB转换为bytes
    factor = (target_size / original_size) ** 0.5  # 使用平方根因子来大致保持图像质量
    
    # 调整图像大小（使用高质量的重采样滤波器）
    img_resized = img.resize((int(img.width * factor), int(img.height * factor)), Image.LANCZOS)
    
    # 将调整大小后的图像转换回bytes流
    output_buffer = BytesIO()
    img_resized.save(output_buffer, format='JPEG', quality=85)  # 使用JPEG格式并设置质量以减小文件大小
    compressed_data = output_buffer.getvalue()
    
    # 将bytes数据重新编码为base64字符串
    compressed_base64 = base64.b64encode(compressed_data).decode('utf-8')
    
    # 计算并打印压缩后的大小
    compressed_size = len(compressed_data)
    print(f"Compressed size: {compressed_size} bytes")
    
    return compressed_base64

@app.post("/doc")
def store_doc(
    collection_name: Optional[str] = Form(None),
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    # "https://www.gutenberg.org/files/1727/1727-h/1727-h.htm"

    log.info(f"file.content_type: {file.content_type}")
    try:
        unsanitized_filename = file.filename
        filename = os.path.basename(unsanitized_filename)

        file_path = f"{UPLOAD_DIR}/{filename}"

        contents = file.file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
            f.close()

        # f = open(file_path, "rb")
        # if collection_name == None:
        #     collection_name = calculate_sha256(f)[:63]
        # f.close()

        # 加载文本内容
        loader, known_type = get_loader(filename, file.content_type, file_path)
        data = ""
        if loader is not None:
            data = loader.load()
        # 加载文件图片
        images = get_images(filename, file_path)

        # delete file
        os.remove(file_path)
        
        return {
            "status": True,
            "collection_name": filename,
            "filename": filename,
            "known_type": known_type,
            "text": data,
            "image": images
        }

        try:
            result = store_data_in_vector_db(data, collection_name)

            if result:
                return {
                    "status": True,
                    "collection_name": collection_name,
                    "filename": filename,
                    "known_type": known_type,
                }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e,
            )
    except Exception as e:
        log.exception(e)
        if "No pandoc was found" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.PANDOC_NOT_INSTALLED,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.DEFAULT(e),
            )


class TextRAGForm(BaseModel):
    name: str
    content: str
    collection_name: Optional[str] = None


@app.post("/text")
def store_text(
    form_data: TextRAGForm,
    user=Depends(get_current_user),
):

    collection_name = form_data.collection_name
    if collection_name == None:
        collection_name = calculate_sha256_string(form_data.content)

    result = store_text_in_vector_db(
        form_data.content,
        metadata={"name": form_data.name, "created_by": user.id},
        collection_name=collection_name,
    )

    if result:
        return {"status": True, "collection_name": collection_name}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES.DEFAULT(),
        )


@app.get("/scan")
def scan_docs_dir(user=Depends(get_admin_user)):
    for path in Path(DOCS_DIR).rglob("./**/*"):
        try:
            if path.is_file() and not path.name.startswith("."):
                tags = extract_folders_after_data_docs(path)
                filename = path.name
                file_content_type = mimetypes.guess_type(path)

                f = open(path, "rb")
                collection_name = calculate_sha256(f)[:63]
                f.close()

                loader, known_type = get_loader(
                    filename, file_content_type[0], str(path)
                )
                data = loader.load()

                try:
                    result = store_data_in_vector_db(data, collection_name)

                    if result:
                        sanitized_filename = sanitize_filename(filename)
                        doc = Documents.get_doc_by_name(sanitized_filename)

                        if doc == None:
                            doc = Documents.insert_new_doc(
                                user.id,
                                DocumentForm(
                                    **{
                                        "name": sanitized_filename,
                                        "title": filename,
                                        "collection_name": collection_name,
                                        "filename": filename,
                                        "content": (
                                            json.dumps(
                                                {
                                                    "tags": list(
                                                        map(
                                                            lambda name: {"name": name},
                                                            tags,
                                                        )
                                                    )
                                                }
                                            )
                                            if len(tags)
                                            else "{}"
                                        ),
                                    }
                                ),
                            )
                except Exception as e:
                    log.exception(e)
                    pass

        except Exception as e:
            log.exception(e)

    return True


@app.get("/reset/db")
def reset_vector_db(user=Depends(get_admin_user)):
    CHROMA_CLIENT.reset()


@app.get("/reset")
def reset(user=Depends(get_admin_user)) -> bool:
    folder = f"{UPLOAD_DIR}"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            log.error("Failed to delete %s. Reason: %s" % (file_path, e))

    try:
        CHROMA_CLIENT.reset()
    except Exception as e:
        log.exception(e)

    return True


if ENV == "dev":

    @app.get("/ef")
    async def get_embeddings():
        return {"result": app.state.EMBEDDING_FUNCTION("hello world")}

    @app.get("/ef/{text}")
    async def get_embeddings_text(text: str):
        return {"result": app.state.EMBEDDING_FUNCTION(text)}
