## Installation & Running locally

1. Clone the repo
2. Create a new virtual environment

```bash
python3 -m venv venv
```
3. Activate the virtual environment

```bash
source venv/bin/activate
```
4. You should be in (venv) now. Cd into project and install dependencies.
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
