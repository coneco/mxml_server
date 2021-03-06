ssh mxml@$1 'ps -ef | grep gunicorn | grep -v grep | cut -c 9-15 | xargs -r kill -9'

ssh mxml@$1 'cd /home/mxml/mxml_server && git pull origin master'
ssh mxml@$1 'cd /home/mxml/mxml_server && git clean -f'
scp ./mxml/mxml/settings_online.py mxml@$1:/home/mxml/mxml_server/mxml/mxml/settings.py

ssh mxml@$1 'cd /home/mxml/mxml_server/mxml && /home/mxml/anaconda3/bin/pip install -r requirements.txt'
ssh mxml@$1 'cd /home/mxml/mxml_server/mxml && /home/mxml/anaconda3/bin/python manage.py collectstatic --noinput'
ssh mxml@$1 'cd /home/mxml/mxml_server/mxml && /home/mxml/anaconda3/bin/python manage.py migrate --noinput'

ssh mxml@$1 'cd /home/mxml/mxml_server/mxml && sh -c "nohup /home/mxml/anaconda3/bin/gunicorn mxml.wsgi > mxml.log 2>&1 &"'
echo 'deploy success'