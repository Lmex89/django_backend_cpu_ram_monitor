how to restore database from dump file 
====================================================
docker exec -i watchserver_db_1 pg_restore -U lmex -d watchserver < <db_dump_name_file>


how to copy file into a docker container 
====================================================
docker cp file_to_copy container_id:volume_folder/


how to dump database from docker container for local dev 
============================================================
docker exec -it 3d915f364388 pg_dump -U lmex watchserver > backu0-db-08-30


how to get inside container db in postgres
============================================================
docker exec -it 3d915f364388 psql -U <user> <db_name>
