# CSPRNG Flask API

This Flask API provides cryptographically secure pseudorandom number generation (CSPRNG) through a simple HTTP interface. The API generates random numbers using OS-specific CSPRNG mechanisms and can be easily extended or integrated into various applications.

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
    git clone https://github.com/yourusername/csprng-flask-api.git
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
python app.py
