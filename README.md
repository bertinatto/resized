# resized

*resized* is a sample application that runs on Kubernetes (Minikube and OpenShift).

It consists of a simple Flask app that takes random images and asynchronously scale them down to 96x96. Celery  and RabbitMQ are used for the asynchronous work. Image tokens are generated and stored in Redis for later retrieval and deletion.

The application itself is very simple, but running all its components under a Kubernetes cluster was an great learning experience. This exercize was suggest to me by Pavel Odvody.

Instruction on how to run *resized* under both Kubernetes (Minikube) and OpenShift can be found in the following files:

```
bin/occtl.sh
bin/k8ctl.sh
```
