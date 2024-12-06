# MMCI export services
Is a an API + a database of BBM Exports from MMCI NIS

## Running the services
1. Go to the `bridgehead` server `/home/export/export-services`
2. Run the API service
```commandline
docker-compose -f compose.prod.yml up -d
```
3. Create DB tables
```commandline
docker-compose exec web python manage.py create_db
```
4. Seed the Static DB data
```commandline
docker-compose exec web python manage.py seed_db
```
5. Seed the MMCI NIS export data
```commandline
docker-compose exec web python manage.py fill_db
```