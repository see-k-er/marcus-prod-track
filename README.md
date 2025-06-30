# marcus-prod-track

Important commands to use - 

to modify pgsql tables
docker exec -it marcus_db psql -U marcus_user -d marcus_db
this should give you the database shell

everytime you modify models.py run make uprade

docker compose down
docker compose build
docker compose up -d 

find the login page at localhost:5001/login
admin123:admin

