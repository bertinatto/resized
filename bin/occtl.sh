#!/bin/bash
# Simple script to start and stop a local OpenShift cluster along with a sample app.

set -x
action=$1
app=$2
d1=/tmp/data01;
d2=/tmp/data02
shift

function start_oc() {
    # First of all, we start the cluster
	oc cluster up &&
    
    # Build the app image
    docker build -t "$app:v1" . &&

    # Temporarly delete all iptables rules
    sudo systemctl stop firewalld

    # Now we create an user called "oc_user". It'll ask for a password
	oc login -u oc_user &&

    # Create a project for the just born user 
	oc new-project $app &&

    # We switch to "system" user and then  we can create the k8 resources.
    # This is only necessary for the Persistent Storage, however,
    # we take the chance to create the other resources as well
	oc login -u system:admin &&
	oc create -f deploy

    # Create temp files for storage
    [ -d $d1 ] || mkdir $d1 && sudo chmod 777 $d1
    [ -d $d2 ] || mkdir $d2 && sudo chmod 777 $d2
}

function stop_oc() {
    # First, we swithc to "system" user so we get permissions to delete
    # Persistent Storage resources
	oc login -u system:admin &&

    # Then we delete everything from our app and shut the cluster down
	oc delete all -l app=$app &&
	oc cluster down

    # Restart firewall
    sudo systemctl restart firewalld

    # Delete temp files
    sudo rm -rf $d1 $d2
}

case $action in
  start)
    start_oc
    ;;
  stop)
      stop_oc
    ;;
  *)
      echo "Not a valid option"
    ;;
esac

