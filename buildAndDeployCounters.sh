# Build
python ./counters.py

# Deploy
IP=`dig +short ps4m.com`
scp -i ~/.ssh/us-west-2.pem var/*.pickle ubuntu@$IP:~/PS4M/var
scp -i ~/.ssh/us-west-2.pem var/duplicateUrlToOriginalid.txt ubuntu@$IP:~/PS4M/var
