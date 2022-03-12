# kubeflow-defaulting
Kubeflow defaulting webhooks

## Installation

### Install [cert-manager](https://cert-manager.io/docs/installation/)

```shell
CERT_MANAGER_VERSION=1.7.1
kubectl apply -f "https://github.com/cert-manager/cert-manager/releases/download/v{CERT_MANAGER_VERSION}/cert-manager.yaml"
```

### Install the webhook
```shell
kubectl apply -k "https://github.com/johnhoman/kubeflow-defaulting/config/default?ref=main"
```