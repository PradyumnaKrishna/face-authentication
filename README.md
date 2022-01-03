<img src="https://raw.githubusercontent.com/PradyumnaKrishna/PradyumnaKrishna/master/logo.svg" align="right" height="50" width="50"/>

# Face Authentication

Face Authentication is an API uses Azure Cognitive Services to identify or verify same persons. This API is implemented using FastAPI.

A [Web Client](https://github.com/PradyumnaKrishna/face-authentication-client) of Face Authentication implemented using Vue.js and JavaScript contains `login` and `registration` features.

## 📖 About
Face Authentication provides a variety of use cases. The primary use case is to verify same person using facial recognition or camera.
API docs are present at `/docs` endpoint of the server.

### Azure Cognitive Services

This API requires Azure Cognitive Services or Azure Face API for the face operations in the image provided. 
[`app/core/face_api.py`](app/core/face_api.py) file contains all operations used by this API such as `detect`, `verify`, `createPersonGroup` etc.

Azure Cognitive Services credentials are required and there is a free tier available on [azure](https://azure.microsoft.com/en-us/services/cognitive-services/face/).
After creating the services, [create a `personGroup`](https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395244) and pass these three credentials (`FACE_API_ENDPOINT`, `FACE_API_KEY`, `FACE_API_GROUP`) to the server using environment variables.

```bash
export FACE_API_ENDPOINT=    # API Endpoint provided by Azure
export FACE_API_KEY=         # API Key provided by Azure
export FACE_API_GROUP=       # Created personGroup ID
```

To read more about Face API, refer to the [docs](https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/).

## ⭐ Getting Started
This codebase can be run using one of three different approaches:
1. Docker
2. Python

### 0. Prerequisites
- Azure Cognitive Services credentials are required.

### 1. Docker
This approach runs an official published image. This approach is not intended for development. It works on Windows, Mac, and Linux.

```bash
# Pull the image from DockerHub
docker pull ipradyumna/face-auth:latest

# Start a container pass required env variables, exposed on port 80 of the host machine
docker run -d -p 8000:80 -e FACE_API_ENDPOINT=<endpoint> -e FACE_API_KEY=<key> -e FACE_API_GROUP=<group> ipradyumna/face-auth:latest
```

### 2. Python
***Note for windows, you are required to install WSL2 and setup the your ide.**

Using [make](https://www.gnu.org/software/make/manual/make.html), install and setup the environment:
```bash
make environment
```

Run the server using
```bash
make start
```

### Debugging
For local debugging, run it and once the server is up, you can easily hit your breakpoints.

If the code fails to run, make sure your Python interpreter is set to use your poetry environment.


## 📝 Documentation
FastApi defaultly has API documentation built in.
- [SwaggerUI](https://github.com/swagger-api/swagger-ui) at [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs) or [`http://localhost:8000/docs`](http://localhost:8000/docs)

## 🤝 Contributing
This project encourages community contributions for development, testing, documentation, code review, and performance analysis, etc.

## 📃 License
This repository is licensed under the [MIT License](LICENSE.md)
