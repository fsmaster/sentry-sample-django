FROM python:3.12-slim
ARG RELEASE=dev
ENV RELEASE=${RELEASE}
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py migrate --noinput
EXPOSE 8080
CMD ["gunicorn", "shop.wsgi", "-b", "0.0.0.0:8080", "-w", "2"]
