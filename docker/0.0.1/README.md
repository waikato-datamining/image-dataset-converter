# image-dataset-converter 0.0.1

## Build

```bash
docker build -t image-dataset-converter:0.0.1 .
```

## Local

### Deploy

* Log into https://aml-repo.cms.waikato.ac.nz with user that has write access

  ```bash
  docker login -u USER public-push.aml-repo.cms.waikato.ac.nz:443
  ```

* Execute commands

  ```bash
  docker tag \
      image-dataset-converter:0.0.1 \
      public-push.aml-repo.cms.waikato.ac.nz:443/tools/image-dataset-converter:0.0.1
      
  docker push public-push.aml-repo.cms.waikato.ac.nz:443/tools/image-dataset-converter:0.0.1
  ```

### Use

* Log into https://aml-repo.cms.waikato.ac.nz with public/public credentials for read access

  ```bash
  docker login -u public --password public public.aml-repo.cms.waikato.ac.nz:443
  ```

* Use image

  ```bash
  docker run --rm -u $(id -u):$(id -g) \
      -v /local/dir:/workspace \
      -it public.aml-repo.cms.waikato.ac.nz:443/tools/image-dataset-converter:0.0.1
  ```

**NB:** Replace `/local/dir` with a local directory that you want to map inside the container. 
For the current directory, simply use `pwd`.


## Docker hub

### Deploy

* Log into docker hub as user `waikatodatamining`:

  ```bash
  docker login -u waikatodatamining
  ```

* Execute command:

  ```bash
  docker tag \
      image-dataset-converter:0.0.1 \
      waikatodatamining/image-dataset-converter:0.0.1
  
  docker push waikatodatamining/image-dataset-converter:0.0.1
  ```

### Use

```bash
docker run --rm -u $(id -u):$(id -g) \
    -v /local/dir:/workspace \
    -it waikatodatamining/image-dataset-converter:0.0.1
```

**NB:** 

* Replace `/local/dir` with a local directory that you want to map inside the container. 
* For the current directory, simply use `pwd`.
* You need to start the docker container with the `--net=host` option if you are using the host's Redis server.
