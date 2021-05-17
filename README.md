## Installation & Running locally

1. Clone the repo
2. Go to the project directory
```bash
cd project
```
3. Create a new virtual environment
```bash
python3 -m venv venv
```
4. Activate the virtual environment
```bash
source venv/bin/activate
```
5. You should be in (venv) now. Install dependencies.
```bash
pip install -r requirements.txt
```
or 
```bash
python3 -m pip install -r requirements.txt
```
5. Run the server locally
```bash
python3 medlink/manage.py runserver db.cse.nd.edu:5001
```
6. View the website in the browser
```bash
db.cse.nd.edu:5001
```
