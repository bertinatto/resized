#!/bin/sh

eval $(minikube docker-env) &&\
kubectl delete -f deploy && \
minikube stop && \
eval $(minikube docker-env -u)

