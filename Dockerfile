# Base image
FROM python:3.9.15-alpine

# Install dependencies
RUN apk upgrade
RUN apk --update \
    add gcc \
    make \
    build-base \
    g++

# RUN rm /var/cache/apk/*

COPY . /website_alerts
WORKDIR /website_alerts
RUN pip3 install -r requirements.txt
RUN python3 /website_alerts/secrets/setup.py build_ext --inplace
RUN rm -rf /website_alerts/secrets
RUN rm -rf /website_alerts/build
RUN rm -r ~/.cache/pip

# Run the application
ENTRYPOINT ["python3", "inlinekeyboard_app.py"]