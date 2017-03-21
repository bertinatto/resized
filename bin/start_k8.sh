#!/bin/bash

set -x
action=$1
app=$2
shift

function start_k8() {
    minikube start --vm-driver=kvm -v3 --logtostderr
    eval $(minikube docker-env)
    docker build -t "app:v1" . && kubectl create -f deploy && sleep 5 && minikube service $app
}

function stop_k8() {
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
