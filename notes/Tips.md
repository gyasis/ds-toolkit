---
noteId: "76021f4068d711eb957d0baddf6fa777"
tags: []

---

## Find and reconnect to a running Jupyter notebook

##### find `jupyter --runtime-dir` -mtime -30 | grep nbserver | xargs cat


## Docker

### run
docker run --rm -it --runtime=nvidia --net=host -v <local dir>:<destination dir> <docker Image id>
### list available dockers
docker images
### list running docker
docker ps
### attach to a running docker
docker exec -it <container id> /bin/bash
### run notebook
jupyter-notebook --ip 0.0.0.0 --allow-root
### commit a docker
docker commit <docker container id> <new docker name>