FROM python:3.9

COPY requirements.txt /requirements.txt
RUN python -m pip install -r /requirements.txt

COPY src /src
ENV PYTHONPATH /src

CMD ["uvicorn","src.main:app","--host=0.0.0.0","--port=8000"]