FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /code

# Install dependencies for running your app (including curl, git, PostgreSQL libraries, and gcc)
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates gnupg curl git libpq-dev gcc

# Copy the requirements.txt to the container
COPY req.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r req.txt

# Copy the entire project into the container
COPY . /code/ 

# Set the PYTHONPATH environment variable to point to the src directory
ENV PYTHONPATH=/code


# Expose the default port (8080 for Cloud Run)
EXPOSE 8080

# Set the command to run the app with uvicorn on port 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
