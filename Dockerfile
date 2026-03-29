# Dockerfile for KAIRA Cognitive Control Architecture Reference Implementation
FROM python:3.10-slim

WORKDIR /app

# Copy dependency file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and evaluation scripts
COPY src/ /app/src/
COPY experiments/ /app/experiments/
COPY data/ /app/data/

# By default, run the benchmark evaluation script
CMD ["python", "experiments/run_experiment.py", "--mode=benchmark"]
