FROM python:3.12.12-alpine3.23

WORKDIR /bin
RUN wget -qO- https://github.com/gitleaks/gitleaks/releases/download/v8.30.0/gitleaks_8.30.0_linux_x64.tar.gz | tar -xz gitleaks

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-deps -r requirements.txt

COPY . .

ENV SERVERLESS=false
EXPOSE 5001

CMD [ "python", "main.py" ]