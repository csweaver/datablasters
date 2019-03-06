# datablasters


## Setup
1. Install Python 3.7 (anaconda distribution)
2. Install requirements
    `pip install -r requirements.txt`
3. Install docker
4. Setup postgres docker container
    ```
    docker pull postgres
    sudo docker run -p 5433:5432 --name datablaster -e POSTGRES_PASSWORD=<pass>  -e POSTGRES_DB=datablaster -d postgres
    ```
5. Set ENV variables
    ```
    export DB_USERNAME=postgres
    export DB_PASSWORD=<password> 
    ```
5. Initialize database
    ```
    cd database
    python build.py
    python load.py
    ```
  
