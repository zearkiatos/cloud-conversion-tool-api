sudo su
git config --global --add safe.directory /home/cloud-conversion-tool/cloud-conversion-tool-api
git checkout master
git pull
sudo docker compose -f=docker-composeVM.yml up --build -d