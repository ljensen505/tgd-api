# The Grapefruits Duo - RESTful API with FastAPI and SQLite

## Overview

The Grapefruits Duo is a RESTful API built with FastAPI and SQLite, providing a simple a simple backend solution for an upcoming React application.

## Installation and Setup

To run the application on Mac or Linux, follow these steps. The steps should be similar on Windows:

<ol>
  <li>Ensure SQLite3 is installed.</li>
  <li>
    Set up a virtual environment:
    <pre><code>python -m venv venv</code></pre>
  </li>
  <li>Create a .env file:<br>
    Create a .env file with the necessary configuration. You can use the .env.example file as a template.
  </li>
  <li>
    Install dependencies:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>
    If <code>app/tgd.db</code> does not exist, create it with:
    <pre><code>python app/seed_db.py</code></pre>
  </li>
  <li>
    Activate the virtual environment:
    <pre><code>source venv/bin/activate</code></pre>
  </li>
</ol>


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