FROM python:3.12-alpine

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --upgrade pip  && \ 
    pip install --no-cache-dir -r requirements.txt

COPY ./app /app  
# Copy the correct app folder

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
