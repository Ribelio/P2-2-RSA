

# CSPRNG Flask API

Instruction for our API documentation, this Flask API provides cryptographically secure pseudorandom number generation (CSPRNG) through a simple HTTP interface. The API generates random numbers using OS-specific CSPRNG mechanisms and can be easily extended or integrated into various applications. The project can also be run in Java with either `RSA\GUI.java` or `CSPRNG\RNGUI.java`.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)
- (Optional) Docker if you prefer containerization

### Steps

1. **Clone the repository**:

    ```bash
    git clone REPO
    cd csprng-flask-api
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the API

To start the Flask API, simply run:

```bash
python CSPRNG\\API_connection.py.py
