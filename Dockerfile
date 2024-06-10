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

RUN ["python", "manage.py", "makemigrations", "app"]
RUN ["python", "manage.py", "migrate"]

# Copy the entrypoint script
COPY entrypoint.sh /code/entrypoint.sh

# Set environment variables for superuser creation
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=adminpassword

# Make entrypoint.sh executable
RUN chmod +x /code/entrypoint.sh

# Entry point to run migrations, create superuser, and start the server
ENTRYPOINT ["./entrypoint.sh"]

# Expose port 8000 for the application
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "food_truck_finder.wsgi:application", "--bind", "0.0.0.0:8000"]
