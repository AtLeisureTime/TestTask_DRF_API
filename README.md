# TestTask_DRF_API
### Run locally
```
git clone https://github.com/AtLeisureTime/TestTask_DRF_API.git
cd TestTask_DRF_API/
python3 -m venv my_env
source my_env/bin/activate
pip install -r requirements.txt

cd TreeMenu/
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata data/mysite_data.json
python manage.py runserver
```
