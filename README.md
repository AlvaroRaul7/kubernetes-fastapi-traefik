# kubernetes-fastapi-traefik

Backend API (Python) in FastApi in a Kubernetes Cluster using Traefik as an API Gateway and Ansible as a configuration management tool.


## Description of the directories

-ansible : Folder with the resources to deploy the traefik pods using Ansible
-kubernetes: Folder with the YAML files to deploy the API and the Postgres Database
-sa-service-2: Folder with the source code of the API


## Requirements for installing the project

- Docker
To install Docker: https://docs.docker.com/desktop/mac/install/
Note: In Docker Desktop Preferences, enable Kubernetes to run the cluster
- Ansible 
To install ansible use pip: `python -m pip install --user ansible`
- Minikube (kubectl)
Follow these steps: https://minikube.sigs.k8s.io/docs/start/
- Python (PIP)
  -  openshift
  -  pyyaml
  -  kubernetes
To install python libraries run Eg: `pip install openshift`
- Helm V3 (Kubernetes Package Manager)
To install run `brew install helm`

## 1.- Steps to start the K8s cluster

**After installing everything above and running Docker Desktop in your PC**
 Run in your terminal:
 1.- `minikube start` (Used to initiate a default local cluster with the default namespace)
 2.- `minikube tunnel` (Used to get an external ip of the cluster to access in the host OS) (Run it in a separate terminal, Don’t close it)
 3.- `kubectl proxy` (Used to forwading the port 8001 to access the k8s dashboard)  
 4.- Go to: http://127.0.0.1:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/#/deployment?namespace=default
 In this URL, you can check that there aren’t any deployments yet in the default namespace.
 
## 2.- Steps to start the Traefik Pods

The Traefik Service is managed by using Ansible, so you can open the file `ansible/templates/traefik_values_default.yml.j2` where you can check that the type
of deployment is a **DaemonSet**


-Traefik listens on port 80 on all interfaces of the host for incoming HTTP requests
-Traefik listens on port 443 on all interfaces of the host for incoming HTTPS request
-Traefik dashboard is enabled and is not exposed to the public internet
Ports exposed:

`ports:
  
  # To access the dashboard you can use "kubectl port-forward" e.g.:
  # kubectl -n traefik port-forward $(kubectl get pods --selector "app.kubernetes.io/name=traefik" --output=name -A | head -1) 9000:9000
  # Opening http://localhost:9000/dashboard/ should show the dashboard.
  traefik:
    port: 9000
    expose: true
    protocol: TCP`

Resources:
`# CPU and RAM resource limits. These settings should also be set to
# reasonable values in case of a memory leak e.g.
resources:
  requests:
    cpu: "100m"
    memory: "50Mi"
  limits:
    cpu: "300m"
    memory: "150Mi"`
    
 In the `ansible/defaults/main.yml`, you can change the namespace for the deployment (Traefik) , name for the ingress controller,etc.
 
 The ansible playbook will detect these settings and apply them to the cluster when it runs the playbook.
 
 In the `ansible/k8s.yml` you can look that the host is traefik. to recognize this dns we need to edit the `/etc/ansible/hosts` file.
 ** If you don’t have the file or folder, please create it using `sudo mkdir /etc/ansible` and `sudo touch hosts` then edit it:
 and paste this:
 
 `[traefik]
  localhost`
  
 We are telling Ansible that the traefik dns will translate to localhost
  
 After doing this we are ready to deploy:
 
 To deploy the Traefik Service in the traefik namespace:
    1.-  `cd ansible`
    2.-  `ansible-playbook --tags=role-traefik-kubernetes --extra-vars action=install k8s.yml`
 One of the final tasks is called `TASK [githubixx.traefik-kubernetes : Output rendered template]`. This allows to check the YAML file before Traefik gets deployed
 If everything is OK , run `kubectl -n traefik get pods -o wide` and you will see a pod with the traefik initials.
 
 To forward the ports to check the traefik dashboard, run:
 `kubectl -n traefik port-forward $(kubectl get pods --selector "app.kubernetes.io/name=traefik" --output=name -A | head -1) 9000:9000`
 
 
