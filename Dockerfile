FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir streamlit==1.32.0 plotly==5.20.0 pandas==2.2.1
COPY app.py .
COPY data/ ./data/
EXPOSE 8506
CMD ["streamlit","run","app.py","--server.port=8506","--server.address=0.0.0.0","--server.headless=true","--browser.gatherUsageStats=false"]
