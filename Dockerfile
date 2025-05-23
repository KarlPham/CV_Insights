FROM python:3.13.2

RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/uploaded_files/resume /app/uploaded_files/jobdesc

EXPOSE 8501

CMD ["streamlit","run","app.py"]
