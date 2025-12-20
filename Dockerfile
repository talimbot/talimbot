# Read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# Dockerfile for TalimBot - AI-Powered Student Grouping System

FROM python:3.11

# Create non-root user (Hugging Face security requirement)
RUN useradd -m -u 1000 user
USER user

# Set environment variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY --chown=user ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the entire backend folder (contains main.py, static files, etc.)
COPY --chown=user ./backend /app/backend

# Copy resources_references folder (optional, for documentation)
COPY --chown=user ./resources_references /app/resources_references

# Expose port 7860 (Hugging Face Spaces requirement)
EXPOSE 7860

# Change to backend directory where main.py is located
WORKDIR /app/backend

# Run the FastAPI application on port 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
