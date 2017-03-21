#!/bin/bash
# Simple script to start and stop a local Kubernetes cluster along with a sample app.

set -x
action=$1
app=$2
shift

function start_k8() {
    # First, we start minikube with a kvm driver. 
    minikube start --vm-driver=kvm -v3 --logtostderr &&

    # Then we load the env variables that tell docker to use
    # the local minikube cluster
    eval $(minikube docker-env) &&

    # Build the app image
    docker build -t "$app:v1" . &&

    # And create all Kubernetes resouces
    kubectl create -f deploy &&

    # Wait a few seconds and open the app in the browser. Kubernetes
    # may take a while more to set up all resources.
    sleep 5 &&
    minikube service $app
}

function stop_k8() {
    # Make sure we're using the minikube cluster, delete all resources we
    # created in the start_k8 function anf finally stop the minikube cluster
    eval $(minikube docker-env)
    kubectl delete -f deploy && minikube stop
}

case $action in
  start)
    start_k8
    ;;
  stop)
      stop_k8
    ;;
  *)
      echo "Not a valid option"
    ;;
esac
