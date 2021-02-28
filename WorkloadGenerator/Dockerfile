FROM python:3.9.1-buster

WORKDIR /usr/src/app
COPY . .
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir -r requirements.txt