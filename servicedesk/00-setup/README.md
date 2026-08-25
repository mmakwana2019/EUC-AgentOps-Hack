# Setup

**Duration:** ~20 minutes

## Goal

Provision a Microsoft Foundry project, deploy a model, and verify authentication — so every later stage can just call the SDK.

## Steps

1. **Create a Foundry project**
   ```bash
   az login
   az extension add -n ml
   az ml workspace create --name euc-agentops-hack --resource-group <your-rg> --kind project
   ```

2. **Deploy a chat model** (e.g. `gpt-4o-mini` or your org's approved deployment) via the Foundry portal: *Deployments → + Deploy model*.

3. **Set environment variables** — copy `.env.example` to `.env` in the repo root:
   ```
   FOUNDRY_PROJECT_ENDPOINT=<your-project-endpoint>
   FOUNDRY_MODEL_DEPLOYMENT=<your-deployment-name>
   AZURE_TENANT_ID=<tenant-id>
   ```

4. **Verify auth**
   ```bash
   python -c "from azure.identity import DefaultAzureCredential; DefaultAzureCredential().get_token('https://management.azure.com/.default'); print('Auth OK')"
   ```

5. **Install dependencies**
   ```bash
   pip install -r ../../requirements.txt
   ```

## Checkpoint

- [ ] Foundry project created and visible in the portal
- [ ] Model deployment shows `Succeeded` status
- [ ] `.env` populated and auth check passes
- [ ] `pip install` completes with no errors

Next: [`01-build-agents/`](../01-build-agents/README.md)
