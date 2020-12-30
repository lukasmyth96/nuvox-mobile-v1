# Runs Django server so it can be accessed on mobile.
sudo ufw enable
sudo ufw allow 8000
# Get IP address to use - might not work for other people.
DJANGO_IP="$(ifconfig wlp2s0 | grep -m1 inet | grep -E -o -m1 "([0-9]{1,3}[\.]){3}[0-9]{1,3}" | head -n 1)"
python manage.py runserver "$DJANGO_IP":8000
