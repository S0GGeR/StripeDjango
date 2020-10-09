## Instruction for UNIX-systems

First of all you need to clone project to local computer. 
```git   
git clone https://github.com/S0GGeR/StripeDjango.git
```    
The next step is initialize the virtual enviroment. I recomend you to use Python 3.8.2
```ssh   
python -m venv venv
```      

Activate your venv:
```ssh   
source venv/bin/activate
```      

After this, go to the repository folder and install all requirments. The command is:    
```python3    
pip install -r req.txt
```

Now make migrations and runserver
```python3    
python manage.py migrate
python manage.py runserver
```

