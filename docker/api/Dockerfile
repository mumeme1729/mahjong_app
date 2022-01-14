FROM python:3.8

WORKDIR /usr/src/server/app
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install pydantic[email]

#CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]