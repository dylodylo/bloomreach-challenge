FROM python:3.10
WORKDIR /bloomreach-challange
COPY requirements.txt /bloomreach-challange/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /bloomreach-challange/requirements.txt
COPY main.py tests.py /bloomreach-challange/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]