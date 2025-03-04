Based on the code snippets you provided, the following technical stack and project directory structure can be inferred.

### **technology stack**

1. **Backend framework**：FastAPI
2. **ORM**：Peewee
3. **database**：Not explicitly specified in the code, but Peevee supports databases such as SQLite, PostgreSQL, MySQL, etc.
4. **Data validation**：Pydantic
5. **Asynchronous HTTP request**：aiohttp
6. **Log management**：logging
7. **middleware**：CORS middleware in FastAPI
8. **Other libraries** likes **`requests`**、**`uuid`**、**`time`**、**`json`** Used for various auxiliary functions

### **Project directory structure**

Based on the code snippet, it can be inferred that the project directory structure may be as follows:

```csharp
CSharp Copy Code
project_root/
│
├── apps/
│   ├── web/
│   │   ├── internal/
│   │   │   └── db.py         # Database initialization and connection
│   │   ├── models/
│   │   │   ├── users.py      # User Model Definition
│   │   │   └── chats.py      # Chats Model definition (speculation)
│   │   └── internal/
│   │       └── db.py         # Database connection configuration
│   └── other_apps/           # Other applications (if any)
│
├── utils/
│   ├── utils.py              # Various practical functions (such as decode_token, get_current user, etc.)
│   ├── misc.py               # Other miscellaneous utility functions (such as get_gravatar_url, etc.)
│
├── config.py                  # Configuration file, containing various constants and configurations
├── constants.py               # Constant definition file, containing error information, etc
├── main.py                    # Main application entrance, FastAPI instance, and routing definition
└── requirements.txt           # Dependency package list

```

### **Specific file content**

- **`apps/web/internal/db.py`**：Define database connection.
    
    ```python
    Copy code in Python
    from peewee import SqliteDatabase
    
    DB = SqliteDatabase('database.db')  # Assuming the use of SQLite database here
    
    ```
    
- **`apps/web/models/users.py`**：Define operations for the User model and user tables.
    
    ```python
    Copy code in Python
    from peewee import *
    from pydantic import BaseModel
    
    class User(Model):
        # Model field definition
        ...
    
        class Meta:
            database = DB
    
    class UserModel(BaseModel):
        # Pydantic Model field definition
        ...
    
    class UsersTable:
        # Definition of User Table Operation Methods
        ...
    
    ```
    
- **`utils/utils.py`**：Define utility functions.
    
    ```python
    Copy code in Python
    def decode_token(token: str):
        # Token decoding logic
        ...
    
    def get_current_user():
        # Retrieve the current user logic
        ...
    
    ```
    
- **`main.py`**：Define FastAPI instances and routes.
    
    ```python
    Copy code in Python
    from fastapi import FastAPI
    from apps.web.models.users import UsersTable
    from config import DB
    
    app = FastAPI()
    Users = UsersTable(DB)
    
    @app.get("/users/")
    def read_users():
        return Users.get_users()
    
    ```
    

### **summarize**

Your project mainly uses FastAPI as the web framework and Peevee as the ORM to interact with the database. The project directory structure reasonably separates model definitions, utility functions, and configuration files, maintaining good organization and maintainability.