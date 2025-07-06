apt install python3.12-venv -y
python3 -m venv botr

source botr/bin/activate
pip install -r requirements.txt
python -m pytest # for some reason tests fail on first run
python -m pytest
rm ./comp_exp.csv
rm ./record.log
rm ./tmptmpRoutes.csv
rm ./tmptmpUsers.csv

# Run in production
while true; do flask run --host=0.0.0.0 -p 80; sleep 10; done
