# kubernetes-fastapi-traefik

Backend API (Python) in FastApi in a Kubernetes Cluster using Traefik as an API Gateway and Ansible as a configuration management tool.


## Description of the directories

- ansible : Folder with the resources to deploy the traefik pods using Ansible
- kubernetes: Folder with the YAML files to deploy the API and the Postgres Database
- sa-service-2: Folder with the source code of the API


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
 - `minikube start` (Used to initiate a default local cluster with the default namespace)
 - `minikube tunnel` (Used to get an external ip of the cluster to access in the host OS) (Run it in a separate terminal, Don’t close it)
 - `kubectl proxy` (Used to forwading the port 8001 to access the k8s dashboard)  
 - Go to: http://127.0.0.1:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/#/deployment?namespace=default
 In this URL, you can check that there aren’t any deployments yet in the default namespace.
 
## 2.- Steps to deploy Traefik using Ansible

The Traefik Service is managed by using Ansible, so you can open the file `ansible/templates/traefik_values_default.yml.j2` where you can check that the type
of deployment is a **DaemonSet**


- Traefik listens on port 80 on all interfaces of the host for incoming HTTP requests
- Traefik listens on port 443 on all interfaces of the host for incoming HTTPS request
- Traefik dashboard is enabled and is not exposed to the public internet.

Ports exposed:

```ports:
  
  # To access the dashboard you can use "kubectl port-forward" e.g.:
  # kubectl -n traefik port-forward $(kubectl get pods --selector "app.kubernetes.io/name=traefik" --output=name -A | head -1) 9000:9000
  # Opening http://localhost:9000/dashboard/ should show the dashboard.
  traefik:
    port: 9000
    expose: true
    protocol: TCP
```

Resources:

```11# CPU and RAM resource limits. These settings should also be set to
# reasonable values in case of a memory leak e.g.
resources:
  requests:
    cpu: "100m"
    memory: "50Mi"
  limits:
    cpu: "300m"
    memory: "150Mi"
 ```
    
 In the `ansible/defaults/main.yml`, you can change the namespace for the deployment (Traefik) , name for the ingress controller,etc.
 
 The ansible playbook will detect these settings and apply them to the cluster when it runs the playbook.
 
 In the `ansible/k8s.yml` you can look that the host is traefik. to recognize this dns we need to edit the `/etc/ansible/hosts` file.
 ** If you don’t have the file or folder, please create it using `sudo mkdir /etc/ansible` and `sudo touch hosts` then edit it:
 and paste this:
 
 ```
 [traefik]
 localhost
 
 ```
  
 We are telling Ansible that the traefik dns will translate to localhost
  
 **After doing this we are ready to deploy**:
 
 To deploy the Traefik Service in the traefik namespace:
 
 -  `cd ansible`
 -  `ansible-playbook --tags=role-traefik-kubernetes --extra-vars action=install k8s.yml`
 
 One of the final tasks is called `TASK [githubixx.traefik-kubernetes : Output rendered template]`. This allows to check the YAML file before Traefik gets deployed
 If everything is OK , run `kubectl -n traefik get pods -o wide` and you will see a pod with the traefik initials.
 
 To forward the ports to check the traefik dashboard, run:
 `kubectl -n traefik port-forward $(kubectl get pods --selector "app.kubernetes.io/name=traefik" --output=name -A | head -1) 9000:9000`
 
 Open:
 http://localhost:9000/dashboard/#/http/services to check that everything is working correctly.
 
 ## Steps to deploy the Postgres Database
 
 To deploy the database in the K8s cluster, we are going to use diferent YAML files.
 
- `cd kubernetes`
 
 In this folder, there are 4 YAML files for the Postgres Deployment.
 
- `postgres-configmap.yaml`  A K8s ConfigMap allows me to save important variables like the name of the db, POSTGRES_USER, POSTGRES_PASSWORD.
- `postgres-storage.yaml`  2 different kinds of volume: PersistentVolume and PersistentVolumeClaim used to preserve the data if a pod is deleted.
- `postgres-service.yaml` A K8s Service that allows me to connect to the Postgres DB and with other pods in the same cluster.
- `postgres-deployment.yaml` A K8s Deployment with a Postgres 10.1 image.
 
 In the kubernetes folder:
 
 Run:
 
- `kubectl apply -f postgres-configmap.yaml`
- `kubectl apply -f postgres-storage.yaml`
- `kubectl apply -f postgres-deployment.yaml`
- `kubectl apply -f postgres-service.yaml`

- If you run `kubectl get all` you can check that everything is deployed.
- Run `kubectl port-forward --namespace default svc/postgres-ip-service 5432:5432` to port forwarding and access the database using `localhost:5432`
- Connect to the database using your favorite DB client like Datagrip, DBeaver,etc.

Inside the users database, run this query:

```
CREATE TABLE rappiuser (
	user_id serial PRIMARY KEY,
	name VARCHAR ( 50 ) UNIQUE NOT NULL,
	lastname VARCHAR ( 50 ) NOT NULL,
	address VARCHAR ( 250 ) NOT NULL,
	phone INTEGER NOT NULL,
	age  INTEGER NOT NULL,
	hire_date DATE,
	fire_date DATE


);

```

That’s all for the db configuration.

## Steps to deploy the FastApi Backend

Finally, the last step is deploying the API. 

- `cd sa-service-2`

Inside the app folder you can check that is structured in models, schemas, services and utils with a main.py file that contains the routes.

Inside the sa-service-2 folder, run:

- `minikube image build -t sa-service-2 . ` 

This command upload the backend image to the minikube local registry, to use it for the deployment.

- `cd ..` return to the previous dir.
- `kubectl apply -f resource-manifests/service-two.yml` Apply a Deployment, Service and an Ingress Controller.

Deployment:

Define the name for the deployment, and the image that will be used `sa-service-2`.

Service:

Define the port that will be exposed in this case is the Port 80

Ingress:

The Ingress Controller will be handled by Traefik and will listen in the port 80

 
Now you can go to http://localhost/docs and start testing the API :)


 
