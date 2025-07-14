### **Technology Stack**

1. **Backend Framework**：FastAPI
2. **ORM**：Peewee
3. **Database**：PostgreSQL。
4. **Data Validation**：Pydantic
5. **Asynchronous HTTP**：aiohttp
6. **Logging**：logging
7. **Middleware**：FastAPI CORS middleware (to handle cross-origin requests).
8. **Utilities**：Standard libraries like requests, uuid, time, json, etc.

### **Project Directory Structure**

A simplified view of how the project might be organized:

```csharp
csharp copy code
project_root/
│
├── apps/
│   ├── web/
│       ├── internal/
│       │   └── db.py         # Database connection setup
│       ├── models/
│       │   ├── users.py      # Defines User model + Pydantic schemas
│       │   └── chats.py      # Could handle chat-related data models
│       └── routers/          # URL routing to handlers
│   
│
├── utils/
│   ├── utils.py              # Core helpers (e.g., decode_token, get_current_user)
│   ├── misc.py               # Miscellaneous utilities (e.g., get_gravatar_url)
│
├── config.py                  # Project-wide settings
├── constants.py               # Reusable constants
├── main.py                    # FastAPI entrypoint
└── requirements.txt           # Python dependencies

```

### **Summary**

This project uses FastAPI + Peewee to build a scalable backend with:
Clear separation of concerns (models, utilities, config).
Automatic data validation via Pydantic.
Support for both synchronous (Peewee) and asynchronous (aiohttp) operations.
The structure keeps the codebase organized, making it easy to extend features (e.g., adding chat endpoints, integrating new databases) or add frontend integrations via FastAPI’s built-in CORS support.