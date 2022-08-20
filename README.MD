how to restore database from dump file 
====================================================
docker exec -i watchserver_db_1 pg_restore -U lmex -d watchserver < backup


how to copy file into a docker container 
====================================================
docker cp file_to_copy container_id:volume_folder/