# Chapter 7: Storage - Practice Labs

## Prerequisites
- A running Kubernetes cluster
- kubectl CLI tool configured
- Basic understanding of Kubernetes storage concepts

## Lab 1: Configuring Pod Storage with EmptyDir
![Configuring Pod Storage with EmptyDir](/Images/chapter06/ch07_lab01_emptydir.png)
### Objective
Create and manage temporary storage between containers using EmptyDir volumes.

### Tasks

1. Create a Pod with shared storage between containers:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: shared-volume-pod
spec:
  containers:
  - name: container1
    image: nginx
    volumeMounts:
    - name: shared-data
      mountPath: /data
  - name: container2
    image: busybox
    command: ["/bin/sh", "-c", "while true; do date >> /data/timestamp.txt; sleep 5; done"]
    volumeMounts:
    - name: shared-data
      mountPath: /data
  volumes:
  - name: shared-data
    emptyDir: {}
```

2. Verify the setup:
```bash
kubectl apply -f shared-volume-pod.yaml
kubectl get pod shared-volume-pod
kubectl exec -it shared-volume-pod -c container1 -- cat /data/timestamp.txt
```

## Lab 2: Working with PersistentVolumes and Claims
![Working with PersistentVolumes and Claims](/Images/chapter06/ch07_lab02_pv_pvc.png)
### Objective
Create and manage persistent storage using PV and PVC.

### Tasks

1. Create a PersistentVolume:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv
spec:
  capacity:
    storage: 2Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
```

2. Create a PersistentVolumeClaim:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

3. Create a Pod using the PVC:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: task-pod
spec:
  containers:
  - name: task-container
    image: nginx
    volumeMounts:
    - name: task-volume
      mountPath: "/usr/share/nginx/html"
  volumes:
  - name: task-volume
    persistentVolumeClaim:
      claimName: task-pvc
```

4. Verify the setup:
```bash
kubectl apply -f task-pv.yaml
kubectl apply -f task-pvc.yaml
kubectl apply -f task-pod.yaml
kubectl get pv,pvc,pod
```

## Lab 3: Implementing Dynamic Volume Provisioning
![Implementing Dynamic Volume Provisioning](/Images/chapter06/ch07_lab03_dynamic_provisioning.png)
### Objective
Set up and use Storage Classes for dynamic volume provisioning.

### Tasks

1. Create a Storage Class:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-storage
provisioner: k8s.io/minikube-hostpath
parameters:
  type: ssd
```

2. Create a PVC using the Storage Class:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
spec:
  storageClassName: fast-storage
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

3. Verify dynamic provisioning:
```bash
kubectl apply -f storage-class.yaml
kubectl apply -f dynamic-pvc.yaml
kubectl get sc,pvc
```

## Lab 4: Storage Troubleshooting Scenarios
![Storage Troubleshooting Scenarios](/Images/chapter06/ch07_lab04_troubleshootingg.png)
### Scenario 1: PVC Binding Issues

1. Check PVC status:
```bash
kubectl get pvc
kubectl describe pvc <pvc-name>
kubectl get events | grep pvc
```

### Scenario 2: Volume Mount Problems

1. Verify Pod volume configuration:
```bash
kubectl describe pod <pod-name>
kubectl get events | grep volume
```

2. Check volume mounts inside container:
```bash
kubectl exec -it <pod-name> -- df -h
kubectl exec -it <pod-name> -- mount | grep <mount-path>
```

## Practice Exercises

1. Create a multi-container Pod with:
   - An EmptyDir volume mounted to multiple containers
   - Different mount paths for each container
   - Verify data sharing between containers

2. Set up persistent storage:
   - Create a PV with specific capacity and access modes
   - Create a matching PVC
   - Create a Pod using the PVC
   - Verify data persistence after Pod deletion

3. Configure dynamic provisioning:
   - Create a custom Storage Class
   - Create multiple PVCs using the Storage Class
   - Verify automatic PV creation

## Cleanup

```bash
# Lab 1
kubectl delete pod shared-volume-pod

# Lab 2
kubectl delete pod task-pod
kubectl delete pvc task-pvc
kubectl delete pv task-pv

# Lab 3
kubectl delete pvc dynamic-pvc
kubectl delete sc fast-storage
```

## Tips for CKA Exam

1. Remember to verify resource creation with `kubectl get` and `kubectl describe`
2. Use `kubectl explain` for quick reference on resource specifications
3. Master the troubleshooting commands for storage issues
4. Practice creating resources both using YAML files and imperative commands