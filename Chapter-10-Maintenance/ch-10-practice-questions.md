# Chapter 10: Maintenance - Practice Questions

## Section 1: Cluster Upgrade Process

### Question 1
During a cluster upgrade, what is the correct order of components to upgrade?

a) kubelet, kubeadm, control plane
b) kubeadm, control plane, kubelet
c) control plane, kubelet, kubeadm
d) kubelet, control plane, kubeadm

**Answer:** b
**Explanation:** The correct upgrade order is:
1. First upgrade kubeadm tool
2. Then upgrade control plane components
3. Finally upgrade kubelet and kubectl on all nodes
4. This ensures proper version compatibility

### Question 2
Given this node status:
```bash
$ kubectl get nodes
NAME        STATUS   VERSION
master-1    Ready    v1.23.0
worker-1    Ready    v1.23.0
worker-2    Ready    v1.22.0
```
What action should you take first for worker-2?

a) Upgrade kubelet immediately
b) Drain the node
c) Cordon the node
d) Restart kubelet service

**Answer:** b
**Explanation:** Before upgrading a node:
1. Drain the node to safely evict workloads
2. Ensure workloads are rescheduled
3. Perform the upgrade
4. Uncordon the node when ready

## Section 2: Backup and Restore

### Question 3
Examine this etcd backup command:
```bash
ETCDCTL_API=3 etcdctl snapshot save backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```
What's missing from this command?

a) Backup location
b) API version
c) Authentication credentials
d) Snapshot name

**Answer:** a
**Explanation:** While the command will work:
1. Should specify full path for backup location
2. Best practice to include timestamp
3. Ensures backup is stored in known location
4. Makes backup management easier

### Question 4
During etcd restore, what must you do first?

a) Stop kube-apiserver
b) Create new data directory
c) Backup existing data
d) Update etcd configuration

**Answer:** a
**Explanation:** Etcd restore process:
1. Stop kube-apiserver to prevent writes
2. Perform the restore operation
3. Update etcd configuration if needed
4. Restart services

## Section 3: Node Maintenance

### Question 5
You need to perform maintenance on a node. Given:
```bash
$ kubectl get pods -o wide
NAME    READY   STATUS    RESTARTS   NODE
pod-1   1/1     Running   0          worker-1
pod-2   1/1     Running   0          worker-1
```
What's the correct command sequence?

a) cordon, drain, maintenance, uncordon
b) drain, maintenance, uncordon
c) cordon, maintenance, uncordon
d) drain, cordon, maintenance, uncordon

**Answer:** b
**Explanation:** Correct sequence:
1. Drain node (automatically cordons)
2. Perform maintenance
3. Uncordon when ready
4. Verify node status

### Question 6
A node drain operation fails with:
```bash
error: cannot delete pods not managed by ReplicationController, ReplicaSet, Job, DaemonSet or StatefulSet
```
What should you add to the drain command?

a) --force
b) --ignore-daemonsets
c) --delete-local-data
d) --grace-period=0

**Answer:** a
**Explanation:** The --force flag:
1. Allows deletion of unmanaged pods
2. Should be used carefully
3. May cause data loss
4. Required for standalone pods

## Section 4: Certificate Management

### Question 7
Your cluster certificates are expiring in 10 days. What command should you use?

a) kubeadm certs renew
b) kubeadm upgrade
c) kubectl certificate approve
d) kubeadm init phase certs

**Answer:** a
**Explanation:** Certificate renewal:
1. Use kubeadm certs renew
2. Can renew all or specific certificates
3. Must be done before expiration
4. Verify with kubeadm certs check-expiration

### Question 8
After certificate renewal, what component needs to be restarted?

a) kubelet
b) etcd
c) kube-apiserver
d) All control plane components

**Answer:** d
**Explanation:** After certificate renewal:
1. All control plane components need restart
2. New certificates must be loaded
3. Can be done by restarting pods
4. Verify component health after restart

## Section 5: Troubleshooting

### Question 9
A node shows NotReady status. Given:
```bash
$ systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
   Active: inactive (dead) since Mon 2023-01-01 12:00:00 UTC; 1h ago
```
What should you check first?

a) Node network
b) Kubelet service
c) System resources
d) Container runtime

**Answer:** b
**Explanation:** For NotReady nodes:
1. Check kubelet service status first
2. Review kubelet logs
3. Verify kubelet configuration
4. Check system resources

### Question 10
During upgrade, pods fail to schedule with error:
```bash
0/3 nodes are available: 1 node(s) had taint {node-role.kubernetes.io/master:NoSchedule}
```
What's the likely cause?

a) Node cordoned
b) Resource constraints
c) Network issues
d) Taint configuration

**Answer:** a
**Explanation:** This occurs when:
1. Node is cordoned during maintenance
2. Pods can't be scheduled
3. Need to uncordon node
4. Verify node status after

### Question 11
Given this scenario:
```bash
$ kubectl get pods -n kube-system
NAME                      READY   STATUS    RESTARTS   AGE
kube-apiserver-master     0/1     Error     3         1h
etcd-master              1/1     Running   0         1h
```
What should you check first?

a) API server logs
b) etcd status
c) Node conditions
d) Network connectivity

**Answer:** a
**Explanation:** For API server issues:
1. Check API server pod logs
2. Verify API server manifest
3. Check certificate validity
4. Monitor resource usage

### Question 12
During node maintenance, you see:
```bash
$ kubectl drain worker-1
error: unable to drain node "worker-1", aborting command...
There are pending nodes to be drained:
 worker-1
error: cannot delete DaemonSet-managed Pods (use --ignore-daemonsets to ignore)
```
What's the correct solution?

a) Delete DaemonSet pods
b) Use --ignore-daemonsets flag
c) Cordon node instead
d) Force pod deletion

**Answer:** b
**Explanation:** When draining nodes:
1. DaemonSet pods must remain
2. Use --ignore-daemonsets flag
3. DaemonSets will recreate pods
4. Safe for node maintenance

### Question 13
Your API server pod is failing with the following error:
```bash
$ kubectl logs kube-apiserver-master -n kube-system
Error: unable to load client CA file: unable to load client CA file: /etc/kubernetes/pki/ca.crt
```
What should you check first?

a) API server manifest
b) Certificate files
c) etcd connection
d) Network connectivity

**Answer:** b
**Explanation:** For API server certificate issues:
1. Verify certificate files exist and are readable
2. Check certificate permissions
3. Validate certificate paths in manifest
4. Ensure certificates haven't expired

### Question 14
During control plane recovery, you notice:
```bash
$ kubectl get componentstatuses
NAME                 STATUS      MESSAGE                                                                                     ERROR
scheduler            Unhealthy   Get "http://127.0.0.1:10251/healthz": dial tcp 127.0.0.1:10251: connect: connection refused
controller-manager   Healthy     ok
etcd-0              Healthy     {"health":"true"}
```
What should you investigate?

a) Scheduler pod logs
b) Scheduler manifest
c) Node status
d) API server configuration

**Answer:** b
**Explanation:** For scheduler issues:
1. Check scheduler static pod manifest
2. Verify scheduler pod is running
3. Review scheduler logs
4. Check port configurations

### Question 15
After restoring etcd from backup, pods aren't being scheduled. Given:
```bash
$ kubectl get nodes
No resources found.
```
What's the likely cause?

a) Node registration lost
b) Scheduler not running
c) Network issues
d) API server down

**Answer:** a
**Explanation:** After etcd restore:
1. Node registrations may be lost
2. Nodes need to re-register with cluster
3. May need to restart kubelet on nodes
4. Verify node certificates

### Question 16
During control plane recovery, you see:
```bash
$ kubectl get pods -n kube-system
NAME                                    READY   STATUS    RESTARTS   AGE
kube-apiserver-master                  1/1     Running   0          1m
kube-controller-manager-master         0/1     Error     3          1m
kube-scheduler-master                  1/1     Running   0          1m
```
What command should you run next?

a) kubectl describe pod kube-controller-manager-master -n kube-system
b) kubectl logs kube-controller-manager-master -n kube-system
c) kubectl delete pod kube-controller-manager-master -n kube-system
d) systemctl restart kubelet

**Answer:** b
**Explanation:** To troubleshoot controller manager:
1. Check pod logs first
2. Look for specific error messages
3. Verify configuration in manifest
4. Check dependencies are running

### Question 17
Your etcd cluster shows:
```bash
$ ETCDCTL_API=3 etcdctl endpoint health
127.0.0.1:2379 is unhealthy: failed to commit proposal: context deadline exceeded
```
What's the first recovery step?

a) Restore from backup
b) Check etcd logs
c) Restart etcd
d) Check disk space

**Answer:** b
**Explanation:** For unhealthy etcd:
1. Check etcd logs for specific errors
2. Verify disk space and I/O
3. Check network connectivity
4. Consider restore if data corrupted

### Question 18
After a node failure, the control plane shows:
```bash
$ kubectl get nodes
NAME     STATUS     ROLES    AGE   VERSION
master   Ready      master   1y    v1.23.0
node1    NotReady   <none>   1y    v1.23.0
node2    Ready      <none>   1y    v1.23.0
```
What should you check on node1?

a) kubelet status
b) Network connectivity
c) System resources
d) All of the above

**Answer:** d
**Explanation:** For NotReady nodes:
1. Check all system components
2. Verify kubelet status and logs
3. Check network connectivity
4. Monitor system resources

### Question 19
During etcd restore, you encounter:
```bash
Error: "etcd-master" already exists
```
What step did you miss?

a) Stopping etcd
b) Moving old data directory
c) Updating etcd manifest
d) Creating backup

**Answer:** b
**Explanation:** Before etcd restore:
1. Move or rename existing data directory
2. Create new directory for restored data
3. Update etcd manifest with new path
4. Restart etcd service

### Question 20
After control plane recovery, you notice:
```bash
$ kubectl get pods
Error from server (Forbidden): pods is forbidden: User "system:node:node1" cannot list resource "pods"
```
What should you check?

a) RBAC configuration
b) Node authorization
c) API server flags
d) Certificate configuration

**Answer:** b
**Explanation:** For node authorization issues:
1. Verify node authorization mode
2. Check node certificates
3. Validate RBAC settings
4. Review API server configuration

### Question 21
In an etcd cluster, you see:
```bash
$ ETCDCTL_API=3 etcdctl endpoint status --cluster
http://10.0.1.10:2379, 8e9e05c52164694d, 3.5.1, 25 MB, true, false, 89, 12369, 12369,
http://10.0.1.11:2379, 8e9e05c52164694e, 3.5.1, 25 MB, false, false, 89, 12369, 12369,
http://10.0.1.12:2379, 8e9e05c52164694f, 3.5.1, 25 MB, false, false, 89, 12369, 12369
```
What does this output indicate?

a) Cluster is healthy
b) Split-brain scenario
c) Version mismatch
d) Data inconsistency

**Answer:** a
**Explanation:** The output shows:
1. All members are on same version (3.5.1)
2. One leader and two followers (true, false, false)
3. Consistent revision numbers (12369)
4. Normal cluster operation

### Question 22
During etcd maintenance, you need to remove a member. What's the correct sequence?

a) Stop etcd, remove member, update configuration
b) Remove member, stop etcd, update configuration
c) Update configuration, remove member, stop etcd
d) Stop member, remove from cluster, update peers

**Answer:** b
**Explanation:** Correct etcd member removal process:
1. Remove member from cluster while it's running
2. Stop etcd on the removed member
3. Update configuration on remaining members
4. Verify cluster health

### Question 23
Your etcd cluster shows high latency. Given:
```bash
$ etcdctl endpoint status
{"level":"warn","ts":"2023-01-01T12:00:00.000Z","caller":"clientv3/retry_interceptor.go:62","msg":"retrying of unary invoker failed","target":"endpoint://client-4c894f87-6ee5-4ca7-8d08-551e2e5c8e34/localhost:2379","attempt":0,"error":"rpc error: code = DeadlineExceeded"}
```
What should you check first?

a) Network connectivity
b) Disk I/O
c) Memory usage
d) CPU utilization

**Answer:** b
**Explanation:** For etcd latency:
1. Check disk I/O performance first
2. etcd is sensitive to disk latency
3. Verify disk IOPS
4. Monitor disk throughput

### Question 24
After adding a new etcd member, you see:
```bash
$ etcdctl member list
{"level":"warn","ts":"2023-01-01T12:00:00.000Z","caller":"clientv3/retry_interceptor.go:62","msg":"retrying of unary invoker failed","target":"endpoint://client-4c894f87-6ee5-4ca7-8d08-551e2e5c8e34/localhost:2379","attempt":0,"error":"context deadline exceeded"}
```
What's the likely cause?

a) Wrong peer URLs
b) Certificate issues
c) Version mismatch
d) Network partition

**Answer:** a
**Explanation:** When adding new etcd members:
1. Verify correct peer URLs configuration
2. Ensure network connectivity between members
3. Check firewall rules
4. Validate cluster configuration

### Question 25
During etcd backup, you see:
```bash
$ ETCDCTL_API=3 etcdctl snapshot save backup.db
Error: rpc error: code = ResourceExhausted desc = etcdserver: request is too large
```
What should you modify?

a) Increase request timeout
b) Adjust quota size
c) Change backup method
d) Reduce concurrent requests

**Answer:** b
**Explanation:** For large etcd databases:
1. Adjust etcd quota size
2. Monitor database size
3. Implement regular compaction
4. Consider incremental backups

### Question 26
Your etcd metrics show:
```bash
etcd_server_proposals_failed_total{cluster_id="14841639068965178418"} > 10
```
What does this indicate?

a) Network issues
b) Quorum loss
c) Disk failure
d) Memory exhaustion

**Answer:** b
**Explanation:** Failed proposals often indicate:
1. Loss of quorum in cluster
2. Unable to commit changes
3. Cluster may be partitioned
4. Member availability issues

### Question 27
After restoring etcd from backup, cluster shows:
```bash
$ etcdctl endpoint health
{"health":"false","reason":"NOSPACE"}
```
What should you do?

a) Increase disk space
b) Defrag the database
c) Compact revisions
d) All of the above

**Answer:** d
**Explanation:** After restore:
1. Ensure sufficient disk space
2. Perform defragmentation
3. Compact old revisions
4. Monitor space usage

### Question 28
In a multi-node etcd cluster, what's the minimum number of healthy members needed for a 5-node cluster to remain operational?

a) 1
b) 2
c) 3
d) 4

**Answer:** c
**Explanation:** For a 5-node cluster:
1. Requires majority (n/2 + 1)
2. 3 nodes minimum for quorum
3. Can tolerate 2 node failures
4. Maintains cluster availability

[Continue with more questions...]
