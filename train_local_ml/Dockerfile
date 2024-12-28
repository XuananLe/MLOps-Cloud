# Sử dụng base image Python
FROM python:3.10-slim

# Copy ứng dụng vào container
WORKDIR /app
COPY . .

# Cài đặt các dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose cổng 8080
EXPOSE 8080

# Chạy Flask app
CMD ["python", "app.py"]
