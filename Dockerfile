FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONPATH=/app

WORKDIR /app

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	gcc \
	make \
	default-libmysqlclient-dev \
	pkg-config \
	&& rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["make", "run"]
