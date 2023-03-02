FROM python:3
ENV TZ="America/Lima"
RUN date
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]

