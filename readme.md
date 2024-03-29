# Nukleus Fullstack Audition

The purpose of this repository is to demonstrate and implement simple inventory management system.

The live site can be visited at https://nukleus-audition.the1375.com

For simplicity, the UI is quite basic and minimal, hence don't expect any fancy UX or animation.

Tech stack being used:

1. Flask (Python 3) for backend
1. Vue 3 (Typescript) for frontend
1. Bootstrap CSS
1. SQLite for database

### Code
The source code is consists of 2 parts:

1. Backend
    - Located at folder `backend-python`
    - For simplicity, all logic and database migration is written in `main.py`
    - To run the backend, ensure you already installed Python 3 and above, `pip` and have `virtualenv` installed in your machine
    - Assuming you are using UNIX environment, inside `backend-python`, run `python -m venv` to install `virtualenv`
    - Run `source venv/bin/activate` to activate `virtualenv`
    - Run `pip install -r requirements.txt` to install required library
    - Run `flask --app=main.py db:seed` for first time database migration and data population
    - Run `python -m flask --app=main.py run --host=localhost --port=5000`. The backend server will be running at `http://localhost:5000`
    - For testing, the code is located at `test.py`. It can be run by `pytest --config-file=test.py test.py`
2. Frontend
    - Located at folder `frontend-vue`
    - To run the frontend, ensure you already installed `node` version 20 and `yarn`
    - Install required dependency by running `yarn install`
    - Run `yarn run dev --port=3000`. The frontend can be browsed at `http://localhost:3000`

### Navigation
The application consists of 3 pages:
1. `/inventory` page
    - This is a main page of the application. It has 3 components; add inventory, search inventory and list of inventory
    - Add inventory will be displayed if user role has `create` permission, while list of inventory will display data if user role has `view` permission

2. `/inventory/{inventoryId}` page
    - This is inventory details page, where user can update the product. It will show the form if user role has `view` permission, and product can be updated or deleted if user has `update` and `delete` permission respectively

3.  `/roles` page
    - This is roles page, where user can add a new role, and list of all roles available with its permissions