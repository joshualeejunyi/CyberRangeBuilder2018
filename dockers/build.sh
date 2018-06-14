docker build -t siab_server .
docker run -p 4200:4200 -e SIAB_USER=testuser -name siab_server siab_sever
