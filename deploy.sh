#!/bin/bash
# Pokemon TCG Analyst - Deployment Script
# This script deploys the application to AWS using SAM

set -e

echo "🚀 Starting deployment process..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if AWS credentials are configured
echo -e "${BLUE}Checking AWS credentials...${NC}"
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo -e "${YELLOW}AWS credentials not found. Configuring...${NC}"
    read -p "Enter AWS Access Key ID: " AWS_ACCESS_KEY_ID
    read -s -p "Enter AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY
    echo ""
    read -p "Enter AWS Region (default: us-east-1): " AWS_REGION
    AWS_REGION=${AWS_REGION:-us-east-1}

    aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
    aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
    aws configure set region "$AWS_REGION"
fi

# Get AWS Account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${GREEN}AWS Account ID: $AWS_ACCOUNT_ID${NC}"

# Install backend dependencies
echo -e "${BLUE}Installing backend dependencies...${NC}"
cd backend
pip install -r requirements.txt -t .
cd ..

# Build SAM application
echo -e "${BLUE}Building SAM application...${NC}"
sam build

# Deploy SAM application
echo -e "${BLUE}Deploying to AWS...${NC}"
sam deploy \
    --stack-name pokemon-tcg-analyst \
    --capabilities CAPABILITY_IAM \
    --region ${AWS_REGION:-us-east-1} \
    --resolve-s3 \
    --parameter-overrides \
        PokemonTCGApiKey=${POKEMON_TCG_API_KEY:-demo-key}

# Get outputs
echo -e "${GREEN}Deployment complete! Getting outputs...${NC}"
API_URL=$(aws cloudformation describe-stacks \
    --stack-name pokemon-tcg-analyst \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
    --output text)

FRONTEND_BUCKET=$(aws cloudformation describe-stacks \
    --stack-name pokemon-tcg-analyst \
    --query 'Stacks[0].Outputs[?OutputKey==`FrontendURL`].OutputValue' \
    --output text)

echo -e "${GREEN}API Endpoint: $API_URL${NC}"
echo -e "${GREEN}Frontend Bucket: $FRONTEND_BUCKET${NC}"

# Build and deploy frontend
echo -e "${BLUE}Building frontend...${NC}"
cd frontend

# Update API URL in build
export REACT_APP_API_URL="$API_URL"
npm install
npm run build

# Deploy to S3
echo -e "${BLUE}Deploying frontend to S3...${NC}"
BUCKET_NAME="pokemon-tcg-analyst-${AWS_ACCOUNT_ID}"
aws s3 sync build/ s3://$BUCKET_NAME/ --delete

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo -e "${GREEN}Frontend URL: http://$BUCKET_NAME.s3-website-${AWS_REGION:-us-east-1}.amazonaws.com${NC}"
echo -e "${GREEN}API URL: $API_URL${NC}"
echo ""
echo -e "${YELLOW}⚠️  Don't forget to configure CORS and any required API keys!${NC}"
