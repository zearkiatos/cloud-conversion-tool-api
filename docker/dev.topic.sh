gcloud pubsub topics create $TOPIC_TASK_POSTED
gcloud pubsub subscriptions create $PUBSUB_SUBSCRIPTION --topic=$TOPIC_TASK_POSTED
gcloud beta emulators pubsub start --host-port=0.0.0.0:8085
tail -f /dev/null