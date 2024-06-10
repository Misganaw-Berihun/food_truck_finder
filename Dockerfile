# Use the official Python image from the Docker Hub
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get install -y libpq-dev

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /code/


# Expose port 8000 for the application
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "food_truck_finder.wsgi:application", "--bind", "0.0.0.0:8000"]
