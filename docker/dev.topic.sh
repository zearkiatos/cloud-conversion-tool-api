gcloud pubsub topics create $TOPIC_TASK_POSTED
gcloud pubsub subscriptions create $PUBSUB_SUBSCRIPTION --topic=$TOPIC_TASK_POSTED
tail -f /dev/null