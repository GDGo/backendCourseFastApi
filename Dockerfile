FROM python:3.11.0

WORKDIR /app

ENV VIRTUAL_ENV "/venv"

RUN python -m venv $VIRTUAL_ENV

ENV PATH "VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

#CMD ["python", "src/main.py"]
CMD alembic upgrade head; python src/main.py
