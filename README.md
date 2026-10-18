# Game Analytics Dashboard

A game analytics application built with Python and FastAPI to track player performance and calculate gaming statistics.

## Features

- Retrieve player statistics through API endpoints
- Calculate player win rates automatically
- Filter players based on their total wins
- Retrieve individual players using their IDs
- Handle missing players with HTTP 404 responses

## Technologies

- Python
- FastAPI
- Git and GitHub

## Running the Application

Install the dependencies:

```bash
pip install "fastapi[standard]"
```

Start the development server:

```bash
fastapi dev main.py
```

Open the API documentation:

http://127.0.0.1:8000/docs

## Project Status

Currently in development. Planned improvements include database integration, additional analytics, and an interactive frontend dashboard.
