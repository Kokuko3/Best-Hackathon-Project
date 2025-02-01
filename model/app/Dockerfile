FROM pytorch/pytorch:latest

COPY ./ /app

WORKDIR /app

COPY ./assets/requirements.txt /app/assets 

RUN pip install -r ./assets/requirements.txt

EXPOSE 8888

# ENTRYPOINT [ "jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser" ]