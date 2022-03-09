traefik-kubernetes
==================

This Ansible role installs [Traefik](https://traefik.io/) edge router for Kubernetes as ingress controller. Behind the doors it uses the official [Helm chart](https://helm.traefik.io/traefik). 

```bash
ansible-playbook --tags=role-traefik-kubernetes --extra-vars action=install k8s.yml
```

To check if everything was deployed use:  `kubectl` commands like `kubectl -n traefik get pods -o wide`


The host `traefik` in the example playbook is most probably just `localhost` specified in Ansible's `hosts` file or whatever host you want to use as "runner" so to say. Just make sure that this host has `helm` installed and has a valid `kubeconfig` (which is normally the case if `kubectl` command works with the Kubernetes cluster).
