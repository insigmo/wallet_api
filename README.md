# Wallet API

## Introduction

This project is a Wallet API designed to manage financial transactions and user accounts. 
The API allows for creating, managing, and querying wallet data efficiently.

## Features
- **Wallet Operations:** Deposit, withdraw, and transfer funds between wallets.
- **Transaction History:** Track all transactions for auditing and reporting.

## Requirements

- Python 3.11+
- MySQL

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/insigmo/wallet_api.git
   cd wallet_api
   ```

## Usage

1. **Run the application:**
   ```bash
   docker-compose up -d web
   ```

2. **Access the API:**
   The API will be available at `http://localhost:8000`. Use tools like Postman or cURL to interact with the endpoints.

## Directory Structure

- **backend/**: Contains backend logic and configurations.
- **build/**: Build-related files.
- **tests/**: Integration tests.
- **utils/**: Utility functions and helpers.
- **wallet_api/**: Main application code.

## API Endpoints

### Wallet Operations

- **List Wallet:** `GET /wallets/`
- **Create Wallet:** `POST /wallets/`

### Transaction History
- **List Transactions:** `GET /transactions/`
- **Create Transaction:** `POST /transactions/`

## Running Tests

To run the tests, use the following command:
```bash
   docker compose up -d web_tests
```
