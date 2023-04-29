# Finance manager
A simple backend to store your daily expense.
## Tech stacks
- Docker Compose
- Python (3.10)
- FastAPI (0.95.0)
- PostgreSQL (14.0)
- ORM: SQLAlchemy
## Installation
- Step 1: Pull the project
- Step 2: In the project root, run: `docker-compose up -d` or if you're using Docker Compose V2, `docker compose up -d`

In case you want to run this as standalone application, you can using the following command: 

```uvicorn financesvc.main:app --reload --host 0.0.0.0 --port 8001```. 

Change your port and ip to fit your requirements.
## Change your configurations
Most of the settings are stored in `docker-compose.yaml` and `financesvc/settings.py`.
You can update database connections if you're using an external database in either docker-compose file or directly in `settings.py`
For CORS settings, you can update your upstream domain in `ALLOW_ORIGINS`.
## Reference
- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://www.sqlalchemy.org/

### Sample front end:
- [finanace-manager-ui](https://github.com/HuyVQ18411c/finance-manager-ui)

