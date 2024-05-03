# our base image
FROM python:latest

# copy the requirements file into the container
COPY requirements.txt .

# install Python dependencies
RUN pip install -r requirements.txt

# copy the rest of the code
COPY . .

# run the application
CMD ["python", "-u", "main.py"]
