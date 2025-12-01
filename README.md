# ⚙️ DocAI Backend Service

The DocAI Backend is a robust API service that powers the DocAI web application, handling all data persistence, business logic, and advanced Large Language Model (LLM) interactions for document generation and refinement.

---

## 🏗️ Architecture and Technology

### Tech Stack

| Component     | Technology         | Description                                        |
| :------------ | :----------------- | :------------------------------------------------- |
| **Framework** | **Flask** (Python) | Micro-framework used for building the API.         |
| **Database**  | **PostgreSQL**     | Primary relational database for data storage.      |
| **ORM**       | **SQLAlchemy**     | Object Relational Mapper for database interaction. |

### Layered Structure

The application logic is organized into three distinct layers to ensure separation of concerns:

1.  **Controllers:** Handle incoming HTTP requests, validate input, call the appropriate service methods, and format the final HTTP responses.
    - **Modules:** `auth`, `project`, `section`, `refinement`.
2.  **Services:** Contain the core business logic, orchestrating actions and communicating with repositories and external systems (like LLMs).
    - **Modules:** `auth`, `project`, `section`, `refinement`, `llm`.
3.  **Repositories:** Manage direct interaction with the database (CRUD operations) via SQLAlchemy.
    - **Modules:** `user`, `project`, `section`, `refinement`, `comment`.

### LLM Handling

The service implements a dedicated LLM component for intelligent content generation and refinement:

- **Context Builder:** Responsible for fetching necessary data from the database (e.g., project details, existing sections, user history) to construct the relevant context for the AI.
- **Prompt Builder:** Takes the generated context, user instructions, and system configuration to construct a well-formed prompt for the LLM API call.
- **LLM Provider:** Configures different LLM providers(Gemini,GPT,Llama) and returns the appropriate provider from a ` ModelRegistry` class

---

## 💾 Database Schema

The backend service interacts with the following core tables in the PostgreSQL database:

- `users`
- `projects`
- `sections`
- `refinements`
- `comments`

---

## 🌐 API Endpoints

The base URL for all API calls is: **`https://localhost:5000/api/v1`**

### 1. Authentication (`/auth`)

| Method | Endpoint         | Description                                                           |
| :----- | :--------------- | :-------------------------------------------------------------------- |
| `POST` | `/auth/login`    | Authenticates a user and returns a JWT token.                         |
| `POST` | `/auth/register` | Creates a new user account.                                           |
| `POST` | `/auth/logout`   | Invalidates the current user's session/token.                         |
| `GET`  | `/auth/me`       | Verifies the token and returns the details of the authenticated user. |

### 2. Projects (`/projects`)

| Method | Endpoint                          | Description                                              |
| :----- | :-------------------------------- | :------------------------------------------------------- |
| `POST` | `/projects`                       | Creates a new project.                                   |
| `POST` | `/projects/generate`              | Generates initial section titles for a project using AI. |
| `GET`  | `/projects`                       | Retrieves a list of all user's projects.                 |
| `GET`  | `/projects/<project_id>`          | Retrieves details for a specific project.                |
| `PUT`  | `/projects/<project_id>`          | Updates the title or other metadata for a project.       |
| `GET`  | `/projects/<project_id>/download` | Exports the project content (Word/PPT).                  |

### 3. Sections (`/sections`)

| Method   | Endpoint                                       | Description                                                        |
| :------- | :--------------------------------------------- | :----------------------------------------------------------------- |
| `POST`   | `/sections/<section_id>/refinements`           | Initiates an iterative refinement on a section's content via chat. |
| `POST`   | `/sections/<section_id>`                       | Updates the manual content of a section.                           |
| `POST`   | `/sections/<section_id>/comments`              | Adds a new comment to a section.                                   |
| `PUT`    | `/sections/<section_id>/comments/<comment_id>` | Updates an existing comment.                                       |
| `DELETE` | `/sections/<section_id>/comments/<comment_id>` | Deletes a comment.                                                 |
| `GET`    | `/sections/<section_id>/regenerate`            | Triggers the complete regeneration of a section's content.         |

### 4. Refinement (`/refinements`)

| Method  | Endpoint                                | Description                                        |
| :------ | :-------------------------------------- | :------------------------------------------------- |
| `PATCH` | `/refinements/<refinement_id>/<rating>` | Rates a specific refinement (`like` or `dislike`). |

---

## 🚀 Running Instructions

The backend service is configured to run securely over HTTPS, requiring a self-signed SSL certificate for local development.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/nizamsalim/docai_backend
    cd docai_backend
    ```
2.  **Install dependencies using Poetry:**
    ```bash
    poetry install
    ```
3.  **Generate SSL Certificate:**
    Use `openssl` to create `cert.pem` and `key.pem` files.
    ```bash
    openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
    ```
4.  **Run the Flask Application:**
    The application will run on `https://localhost:5000`.
    ```bash
    poetry run flask run --cert=cert.pem --key=key.pem
    ```

---

## 🔒 Environment Variables

The following environment variables must be configured for the application to run correctly:

| Variable Name    | Example Value                             | Description                                          |
| :--------------- | :---------------------------------------- | :--------------------------------------------------- |
| `FLASK_APP`      | `docai_backend.app`                       | Specifies the main Flask application module.         |
| `FLASK_ENV`      | `production`                              | Sets the running environment.                        |
| `FLASK_DEBUG`    | `0`                                       | Disables debug mode in a production environment.     |
| `DATABASE_URL`   | `postgresql://user:pass@host:port/dbname` | Full URI for connecting to the PostgreSQL database.  |
| `JWT_SECRET`     | `your_long_secure_secret_key`             | Secret key used to sign and verify JSON Web Tokens.  |
| `GEMINI_API_KEY` | `AIzaSy...`                               | API key for accessing the Gemini model.              |
| `GROQ_API_KEY`   | `gsk_...`                                 | API key for accessing the Groq models (e.g., Llama). |
