FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir requests tkinter
RUN pip install pygame

CMD ["python", "PetAudio.py"]