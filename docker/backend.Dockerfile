FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "backend.app:app", "--workers", "3", "--bind", "0.0.0.0:5000", "--log-level", "info"]
