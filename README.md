# ShareBoard

## Project Description

ShareBoard is a real-time collaborative scratchpad application built with FastAPI and WebSockets. It allows multiple users to connect to the same session and see each other's changes in real-time. This project provides a simple and efficient way to share ideas, notes, and code snippets with others.

## Features

*   Real-time collaboration using WebSockets 
*   Simple and intuitive user interface
*   Dark and light theme support
*   Collapsible sidebar for settings

## Dependencies

*   FastAPI
*   Uvicorn
*   SQLAlchemy
*   PostgreSQL
*   Python-dotenv
*   Alembic
*   websockets

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd shareBoard
    ```

2.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the database:**

    *   Ensure you have PostgreSQL installed and running.
    *   Create a `.env` file with the following variables:

        ```
        DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>:<port>/<database>
        ```

        Replace `<user>`, `<password>`, `<host>`, `<port>`, and `<database>` with your PostgreSQL credentials.
    *   Run Alembic migrations to create the database tables:

        ```bash
        alembic upgrade head
        ```

## Running the Application

1.  **Start the Uvicorn server:**

    ```bash
    uvicorn app.main:app --reload
    ```

    This will start the server on `http://localhost:8000`.

2.  **Open the application in your browser:**

    Navigate to `http://localhost:8000` in your web browser.

## API Endpoints

*   **GET `/`**: Serves the main HTML page.
*   **GET `/ws/{session_id}`**: WebSocket endpoint for real-time communication.

## Docker

1.  **Build the Docker image:**

    ```bash
    docker build -t shareboard .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 shareboard
    ```

## Docker Compose

1.  **Run the application using Docker Compose:**

    ```bash
    docker-compose up --build
    ```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.