FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid 1000 --home-dir /home/app --create-home app

COPY --chown=app:app yago/ /app
COPY --chown=app:app  requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --no-input

USER app

# Make port 5000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "yago.wsgi"]
