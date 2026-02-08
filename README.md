# mcp-kube-demo

In this demo, we run an **AI agent** and an **MCP (Model Context Protocol) server** inside Kubernetes, and show that the agent can **dynamically discover and call tools at runtime using MCP** — without hardcoding any tool logic.

**Key idea:**  
> The agent does not know what tools exist ahead of time — it asks MCP at runtime.

---

## Prerequisites

You need the following installed on your machine:

- Docker
- kubectl
- kind (recommended for local Kubernetes)

**Verify your setup:**

```
docker --version
kubectl version --client
kind version
```

**Create a Kubernetes Cluster**
Create a local Kubernetes cluster using kind:
```
kind create cluster --name mcp-demo-final
kubectl cluster-info --context kind-mcp-demo-final
Load the MCP Server Image into kind
```

Kind runs Kubernetes nodes inside Docker containers, so locally built images must be explicitly loaded into the cluster.
```
kind load docker-image mcp-server:demo --name mcp-demo-final
```

Sanity check that the image exists locally:
```
docker images | grep mcp-server
```

**Deploy the MCP Server to Kubernetes**
Apply the MCP server manifests:
```
kubectl apply -f mcp-server.yaml
```

Wait for the deployment to become ready:
```
kubectl rollout status deployment/mcp-server
kubectl get pods -l app=mcp-server
kubectl get svc mcp-server
```

At this point, the MCP server is running inside the cluster and is discoverable via Kubernetes DNS.

**Run the Agent**
Deploy the agent pod:
```
kubectl apply -f agent.yaml
kubectl get pod agent -w
```

Once the agent finishes running, view its logs:
```
kubectl logs agent
```

**Expected Output**
```
🔍 Discovering tools via MCP...
- get_time: Get the current server time
- get_cluster_name: Return the Kubernetes cluster name

⚙️ Calling tool: get_cluster_name
✅ Tool result: {'cluster': 'demo-cluster'}
```

**What This Demo Shows**
- The agent queried the MCP server at runtime
- The available tools were discovered dynamically
- The agent selected the best tool based on availability
- The tool was executed via MCP
- No tools were hardcoded into the agent.

**Key Takeaway**
MCP allows agents to dynamically discover and use tools at runtime, while Kubernetes provides the runtime, networking, and isolation needed to run this safely in production.

**Cleanup (Optional)**
Delete the demo resources and cluster:
```
kubectl delete -f agent.yaml
kubectl delete -f mcp-server.yaml
kind delete cluster --name mcp-demo-final
```
