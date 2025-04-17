# Comands

-  docker build -t x-startup-deployment .       
- docker tag x-startup-deployment europe-west3-docker.pkg.dev/x-startup-discover/x-startup-repo/x-startup-deployment
- docker push europe-west3-docker.pkg.dev/x-startup-discover/x-startup-repo/x-startup-deployment
- docker run -d  -p 3000:8080  --env-file .env --name x-startup-deployment  x-startup-deployment
-  pip freeze > requirements.txt                  
