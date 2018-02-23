pip3 install -r reqs.txt
sudo docker build -t kafzoo:portsopen .
sudo docker run -d --network=host kafzoo:portsopen
python3 chat_app.py
