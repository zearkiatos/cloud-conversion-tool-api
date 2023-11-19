FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:alpine

COPY ./key/service-account-key.json /key/service-account-key.json

RUN gcloud auth activate-service-account --key-file=/key/service-account-key.json

RUN gcloud config set project miso-cloud-solutions-for-test

RUN gcloud services enable pubsub.googleapis.com

RUN gcloud components install pubsub-emulator

EXPOSE 8085

COPY ./docker /docker