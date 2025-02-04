# ASCOR API

Welcome to the ASCOR API repository! This project is part of the [DS205 course](https://lse-dsi.github.io/DS205) and is designed to help you build and deploy APIs for analysing and serving the ASCOR dataset.

## Getting Started

### 1. Clone the Repository
To get started, clone this repository to your local machine:
```bash
git clone https://github.com/lse-ds205/ascor-api.git
cd ascor-api
```

### 2. Install Dependencies
Ensure you have Python 3.10+ installed. Use the following command to install all required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI App
Navigate to the `v1/` folder and start the server:
```bash
cd v1
uvicorn app:app --reload
```

Visit `http://127.0.0.1:8000` in your browser to test the default endpoint. You can explore the interactive API documentation at `http://127.0.0.1:8000/docs`.


## Running the API

1. Make sure you have all dependencies installed:
```bash
pip install fastapi uvicorn pandas openpyxl
```

2. To run the API in development mode with auto-reload:
```bash
uvicorn v1.app:app --reload
```

Note: The command structure is `uvicorn [module_path]:[fastapi_instance_name] --reload`
- `v1.app` refers to the `app.py` file in the `v1` directory
- `app` refers to the FastAPI instance created in that file
- `--reload` enables auto-reloading when code changes

The API will be available at:
- Local: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs

## Available Endpoints

- `GET /` - Root endpoint (Hello World)
- `GET /v1/country-data/{country}/{assessment_year}` - Get country assessment data

## Collaborator Access

Students who are currently enrolled in the DS205 course (or auditing) are eligible to contribute to this repository. To be granted push permission on this repository, please send a message to Jon on Slack with your GitHub username. Once approved, you'll receive an invite to contribute.

## Need Help?
For issues or questions:
- Post in the `#help` channel on Slack.
- Check out the [FastAPI Documentation](https://fastapi.tiangolo.com/).
- Contact Jon directly if you face persistent issues.