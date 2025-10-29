# Use official Python 3.11 slim image
FROM python:3.11-slim

# Create a non-root user
RUN useradd -m appuser
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Change ownership
RUN chown -R appuser /app
USER appuser

# Expose health check port
EXPOSE 8080

# Run the bot
CMD ["python", "bot.py"]
