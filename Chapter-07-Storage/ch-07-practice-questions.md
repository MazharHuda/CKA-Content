# Chapter 7: Storage - Practice Questions

## Section 1: Basic Storage Concepts

### Question 1
Which volume type is best suited for sharing data between containers in the same pod that is deleted when the pod is removed?

a) hostPath
b) emptyDir
c) persistentVolume
d) configMap

**Answer:** b
**Explanation:** emptyDir is a temporary volume type that is created when a Pod is assigned to a node and exists as long as that Pod is running on that node. When the Pod is removed, the emptyDir is deleted permanently.

### Question 2
Given this pod configuration:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
  - name: test-container
    image: nginx
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir:
      sizeLimit: 500Mi
```
What happens if the container tries to write more than 500Mi to the volume?

a) The write will fail
b) The pod will be evicted
c) The volume will automatically expand
d) The data will be compressed

**Answer:** b
**Explanation:** When a sizeLimit is set for an emptyDir volume and the usage exceeds this limit, the pod will be evicted from the node.

## Section 2: Persistent Volumes and Claims

### Question 3
Examine this PersistentVolume configuration:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-demo
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: "/mnt/data"
```
What happens to the data when this PV is released from its claim?

a) The data is immediately deleted
b) The data is preserved and the volume becomes available for new claims
c) The data is preserved but the volume remains unavailable for new claims
d) The data is backed up automatically

**Answer:** c
**Explanation:** With reclaimPolicy: Retain, when a PersistentVolumeClaim is deleted, the PersistentVolume retains the data but remains unavailable for other claims until manually reclaimed by an administrator.

### Question 4
You have a PVC stuck in "Pending" state. Given:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-claim
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 5Gi
```
What could be the cause?

a) No PV available with matching storage size
b) No PV available with matching access mode
c) Storage class not specified
d) Any of the above

**Answer:** d
**Explanation:** A PVC can remain in "Pending" state for multiple reasons:
1. No available PV matches the requested size
2. No PV supports the requested access mode (ReadWriteMany)
3. No default storage class and none specified in the PVC

## Section 3: Storage Classes

### Question 5
Given this StorageClass:
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
volumeBindingMode: WaitForFirstConsumer
```
When will the PersistentVolume be created?

a) Immediately when a PVC is created
b) When a pod using the PVC is scheduled
c) When the storage class is created
d) When the first write occurs

**Answer:** b
**Explanation:** With volumeBindingMode: WaitForFirstConsumer, volume binding and provisioning is delayed until a pod using the PVC is created and scheduled to a node.

### Question 6
What is the purpose of the default storage class annotation?
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
```

a) Makes the storage class immutable
b) Automatically assigns this storage class to PVCs without a specified class
c) Provides better performance
d) Enables dynamic provisioning

**Answer:** b
**Explanation:** The annotation storageclass.kubernetes.io/is-default-class: "true" marks this storage class as the default. PVCs that don't specify a storage class will automatically use this one.

## Section 4: Advanced Storage Scenarios

### Question 7
You need to expand a PVC. Given:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  resources:
    requests:
      storage: 10Gi
  storageClassName: expandable
```
What conditions must be met for successful expansion?

a) The storage class must allow volume expansion
b) The pod using the PVC must be deleted first
c) The PV must have sufficient capacity
d) Both a and c

**Answer:** d
**Explanation:** Volume expansion requires:
1. The storage class must have allowVolumeExpansion: true
2. The underlying PV must support expansion
3. The requested size must not exceed available capacity

### Question 8
In a StatefulSet using volumeClaimTemplates, what happens to the PVCs when the StatefulSet is deleted?

a) PVCs are automatically deleted
b) PVCs remain and must be manually deleted
c) PVCs are archived
d) PVCs are marked as inactive

**Answer:** b
**Explanation:** When a StatefulSet is deleted, its PVCs are not automatically deleted. This is by design to prevent accidental data loss. The PVCs must be manually deleted if the data is no longer needed.

## Section 5: Troubleshooting Scenarios

### Question 9
A pod is stuck in ContainerCreating state with the following event:
```
MountVolume.SetUp failed for volume "pvc-volume" : mount failed: exit status 32
```
What should you check first?

a) PVC binding status
b) Node disk space
c) Storage class configuration
d) Pod security context

**Answer:** a
**Explanation:** When a pod is stuck in ContainerCreating with mount failures, first verify:
1. PVC exists and is bound
2. PV is available and accessible
3. Check events using kubectl describe pvc and kubectl describe pv

### Question 10
You have a pod using a hostPath volume that can't access its data. Given:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
  - name: test-container
    image: nginx
    volumeMounts:
    - mountPath: /data
      name: test-volume
  volumes:
  - name: test-volume
    hostPath:
      path: /data
      type: DirectoryOrCreate
```
What should you verify?

a) Directory permissions on the host
b) Pod security context
c) Node selector configuration
d) All of the above

**Answer:** d
**Explanation:** For hostPath volumes, verify:
1. Directory exists and has correct permissions on the host
2. Pod security context allows access to the directory
3. Pod is scheduled on the correct node
4. SELinux/AppArmor policies if enabled

### Question 11
Given this StatefulSet configuration:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
  replicas: 3
  template:
    spec:
      containers:
      - name: nginx
        image: nginx
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```
How many PVCs will be created?

a) 1
b) 2
c) 3
d) 0

**Answer:** c
**Explanation:** StatefulSet creates one PVC per replica using the volumeClaimTemplate. With replicas: 3, three PVCs will be created, named www-web-0, www-web-1, and www-web-2.

### Question 12
You need to migrate data from one PV to another. Which approach is correct?

a) Copy data directly between PVs
b) Create a pod with both PVCs mounted and copy data
c) Use kubectl cp command
d) Modify the PVC to point to new PV

**Answer:** b
**Explanation:** To migrate data between PVs:
1. Create a pod that mounts both the source and destination PVCs
2. Use standard file copying tools within the pod
3. Ensure data integrity during copy
4. Update application to use new PVC

### Question 13
Examine this storage configuration:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteMany
  nfs:
    server: nfs-server.default.svc.cluster.local
    path: "/exports"
```
Which statement is true about this PV?

a) Only one pod can mount this volume at a time
b) Multiple pods can mount this volume read-only
c) Multiple pods can mount this volume with read-write access
d) The volume can only be mounted on one node

**Answer:** c
**Explanation:** The ReadWriteMany access mode allows the volume to be mounted by multiple pods with read-write access, which is commonly used with NFS volumes for shared storage across pods.

### Question 14
Your pod fails to start with the error:
```
Unable to mount volumes for pod: timeout expired waiting for volumes to attach/mount
```
Given this PVC:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: slow-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
  storageClassName: standard
```
What could be the issue?

a) PVC size too large
b) Storage class doesn't exist
c) Volume attachment timeout
d) Any of the above

**Answer:** d
**Explanation:** This error can occur due to multiple reasons:
1. Requested storage size exceeds available capacity
2. Storage class issues or misconfiguration
3. Volume attachment taking longer than the timeout period
4. Storage provider issues

### Question 15
You have a pod using a ReadWriteOnce (RWO) PVC and need to run the pod on multiple nodes. What's the best solution?

a) Change the access mode to ReadWriteMany
b) Create multiple PVCs
c) Use a different storage type
d) Mount the volume as read-only

**Answer:** a
**Explanation:** For pods running on multiple nodes that need write access to the same volume:
1. Use ReadWriteMany (RWX) access mode
2. Choose a storage provider that supports RWX (e.g., NFS)
3. Modify the PV and PVC configurations accordingly

### Question 16
Given this scenario:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Delete
  storageClassName: manual
  hostPath:
    path: "/mnt/data"
```
What happens to the data when the associated PVC is deleted?

a) Data is preserved and volume becomes available
b) Data and volume are both deleted
c) Only the volume is deleted
d) Data is archived

**Answer:** b
**Explanation:** With persistentVolumeReclaimPolicy: Delete:
1. When PVC is deleted, the PV is automatically deleted
2. All data in the volume is deleted
3. The storage resource is reclaimed
4. A new PV must be created for future use

### Question 17
Your storage class configuration includes:
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: delayed-binding
spec:
  volumeBindingMode: WaitForFirstConsumer
  provisioner: kubernetes.io/gce-pd
```
What is the advantage of this configuration?

a) Faster volume provisioning
b) Better resource utilization
c) Improved security
d) Enhanced performance

**Answer:** b
**Explanation:** WaitForFirstConsumer binding mode provides:
1. Better resource utilization by delaying volume creation
2. Topology-aware volume provisioning
3. Avoids creating volumes that might never be used
4. Reduces cloud provider costs

### Question 18
A pod using a PVC remains in Pending state. The PVC shows:
```bash
$ kubectl describe pvc my-claim
...
Status:    Pending
Capacity:  
Access Modes:  
Events:
  Warning  ProvisioningFailed  2s    persistentvolume-controller  Failed to provision volume: storage class "fast" not found
```
What's the most likely cause?

a) Insufficient storage capacity
b) Missing storage class
c) Invalid access mode
d) Network issue

**Answer:** b
**Explanation:** The error indicates:
1. The specified storage class doesn't exist
2. Check storage class existence: kubectl get storageclass
3. Either create the missing storage class
4. Or modify PVC to use an existing storage class

### Question 19
You need to expand a volume in use by a pod. Given:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  resources:
    requests:
      storage: 5Gi
```
What's the correct procedure?

a) Delete and recreate the PVC
b) Edit the PVC spec directly
c) Create a new larger PVC and migrate data
d) Use kubectl patch to update storage size

**Answer:** d
**Explanation:** To expand a volume:
1. Verify storage class allows expansion
2. Use kubectl patch or edit to increase size
3. Wait for resize to complete
4. Verify new size is available to pod

### Question 20
In a production environment, what's the recommended way to handle sensitive data in volumes?

a) Use emptyDir with encryption
b) Use Secrets mounted as volumes
c) Use encrypted PVs
d) Use hostPath with restricted permissions

**Answer:** b
**Explanation:** For sensitive data:
1. Use Kubernetes Secrets mounted as volumes
2. Ensure Secret encryption at rest is enabled
3. Implement proper RBAC controls
4. Consider using external secret management systems

[Continue with more questions if needed...]
