#!/bin/bash
# Todo App Blueprint Deployment Script
# Deploys complete todo application stack to Kubernetes

set -e

# Configuration
NAMESPACE="${NAMESPACE:-default}"
RELEASE_NAME="${RELEASE_NAME:-todo-app}"
HELM_CHART_PATH="../../helm/todo-evolution"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Todo App Blueprint Deployment${NC}"
echo "=================================="

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --cluster-name)
      CLUSTER_NAME="$2"
      shift 2
      ;;
    --database-url)
      DATABASE_URL="$2"
      shift 2
      ;;
    --domain)
      DOMAIN="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN="--dry-run"
      shift
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Validate required parameters
if [ -z "$DATABASE_URL" ]; then
  echo -e "${YELLOW}Warning: DATABASE_URL not set, using placeholder${NC}"
  DATABASE_URL="postgresql+asyncpg://user:pass@host/db"
fi

if [ -z "$DOMAIN" ]; then
  DOMAIN="todo.local"
fi

echo -e "\n${GREEN}Configuration:${NC}"
echo "  Namespace: $NAMESPACE"
echo "  Release: $RELEASE_NAME"
echo "  Domain: $DOMAIN"
echo ""

# Step 1: Create namespace if needed
echo -e "${GREEN}Step 1: Ensuring namespace exists...${NC}"
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Step 2: Deploy Dapr components
echo -e "${GREEN}Step 2: Deploying Dapr components...${NC}"
kubectl apply -f ../../dapr/components/ -n $NAMESPACE $DRY_RUN

# Step 3: Deploy with Helm
echo -e "${GREEN}Step 3: Deploying with Helm...${NC}"
helm upgrade --install $RELEASE_NAME $HELM_CHART_PATH \
  --namespace $NAMESPACE \
  --set secrets.databaseUrl="$DATABASE_URL" \
  --set secrets.betterAuthSecret="${BETTER_AUTH_SECRET:-change-me}" \
  --set secrets.openaiApiKey="${OPENAI_API_KEY:-sk-placeholder}" \
  --set ingress.host="$DOMAIN" \
  --wait \
  $DRY_RUN

# Step 4: Wait for rollout
if [ -z "$DRY_RUN" ]; then
  echo -e "${GREEN}Step 4: Waiting for deployment...${NC}"
  kubectl rollout status deployment/todo-backend -n $NAMESPACE --timeout=120s
  kubectl rollout status deployment/todo-frontend -n $NAMESPACE --timeout=120s
fi

# Step 5: Display access information
echo -e "\n${GREEN}✅ Deployment Complete!${NC}"
echo "=================================="
echo ""
echo "Access your application:"
echo "  Frontend: http://$DOMAIN"
echo "  Backend API: http://$DOMAIN/api"
echo "  API Docs: http://$DOMAIN/docs"
echo ""
echo "View pods:"
echo "  kubectl get pods -n $NAMESPACE"
echo ""
echo "View logs:"
echo "  kubectl logs -f deployment/todo-backend -n $NAMESPACE"
