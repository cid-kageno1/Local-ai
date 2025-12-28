# Use a slim version of Python to keep the build fast
FROM python:3.9-slim

# Create a non-root user (Hugging Face requirement)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory
WORKDIR $HOME/app

# Copy and install dependencies first (for faster rebuilding)
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of your app files
COPY --chown=user . .

# Expose the default Hugging Face port
EXPOSE 7860

# Run using Gunicorn (Production-grade server)
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
