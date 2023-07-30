# The Grapefruits Duo - RESTful API with FastAPI and SQLite

## Overview

The Grapefruits Duo is a RESTful API built with FastAPI and SQLite, providing a simple a simple backend solution for an upcoming React application.

## Installation and Setup

To run the application on Mac or Linux, follow these steps:

1. Set up a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Create a .env file:<br>
Create a .env file with the necessary configuration. You can use the .env.example file as a template.

3. Install dependencies:
    ```bash
   pip install -r requirements.txt
   ```

4. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```

## Running the application

To start the application, execute the following command:

```bash
uvicorn app.main:app --reload
```

## Testing

To run the test suite, execute the following command.:

```bash
pytest
```

Or, if you desire stdout to be shown:

```bash
pytest -rP
```