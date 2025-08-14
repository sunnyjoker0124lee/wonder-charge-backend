# Wonder Charge Backend (Flask)

This is the backend service for the Wonder Charge event management system, built with Flask. It provides a RESTful API for managing event tasks, supporting multi-user collaboration and data synchronization.

## Features

- **Task Management**: CRUD operations for event tasks (create, read, update, delete).
- **PostgreSQL Database**: Uses PostgreSQL for persistent data storage, ensuring data integrity and consistency.
- **Multi-user Collaboration**: Supports real-time data synchronization for collaborative work.
- **CORS Enabled**: Allows cross-origin requests from the frontend application.

## Technologies Used

- **Python 3.11**
- **Flask**: Web framework
- **psycopg2-binary**: PostgreSQL adapter for Python
- **python-dotenv**: For managing environment variables

## Setup and Installation (Local Development)

1.  **Clone the repository**:
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd wonder_charge_backend
    ```

2.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup**:
    *   **PostgreSQL**: Ensure you have a PostgreSQL server running. Create a database for this application.
    *   Create a `.env` file in the `wonder_charge_backend` directory with your database connection string:
        ```
        DATABASE_URL="postgresql://user:password@host:port/database_name"
        ```
        (Example: `postgresql://postgres:mysecretpassword@localhost:5432/wonder_charge_db`)
    *   **SQLite (for local development/testing without PostgreSQL)**: If `DATABASE_URL` is not set, the application will default to using a local SQLite database (`tasks.db`).

5.  **Initialize the database and migrate data (optional, for initial setup)**:
    ```bash
    python migrate_data.py
    ```
    This script will create the necessary tables and populate them with initial data from `excel_data.json`.

6.  **Run the application**:
    ```bash
    python src/main.py
    ```
    The server will run on `http://0.0.0.0:5000` (or the port specified in your environment variables).

## API Endpoints

- `GET /api/tasks`: Get all tasks.
- `POST /api/tasks`: Create a new task.
- `PUT /api/tasks/<id>`: Update an existing task.
- `DELETE /api/tasks/<id>`: Delete a task.

## Deployment (Render)

Refer to the Render deployment guide for detailed instructions on deploying this Flask application as a Web Service on Render. Ensure your `DATABASE_URL` environment variable is correctly set on Render to connect to your PostgreSQL database.

---

