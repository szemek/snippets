#!/bin/bash

kubectl run  -it ubuntu --image=ubuntu:latest --restart=Never --rm -- /bin/bash
apt-get update && apt-get install -y curl unzip less
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -qq awscliv2.zip
./aws/install
aws sts get-caller-identity

# override spec with custom service account
kubectl run -it ubuntu --image=ubuntu:latest --labels="run_on=fargate" --restart=Never --rm --overrides='
{
  "apiVersion": "v1",
  "spec": {
    "serviceAccountName": "my-service-account"
  }
}
' -- /bin/bash
