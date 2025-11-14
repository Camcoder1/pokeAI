#!/bin/bash
# Quick deployment using AWS CLI only (no SAM required)

set -e

echo "🚀 Quick Deploy - Pokemon TCG Analyst"
echo "====================================="
echo ""

AWS_REGION="us-east-1"
STACK_NAME="pokemon-tcg-analyst"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "AWS Account: $ACCOUNT_ID"
echo "Region: $AWS_REGION"
echo ""

# Step 1: Create deployment bucket
echo "Step 1: Creating S3 bucket for deployment..."
DEPLOY_BUCKET="pokemon-tcg-deploy-${ACCOUNT_ID}"
aws s3 mb s3://$DEPLOY_BUCKET --region $AWS_REGION 2>/dev/null || echo "Bucket already exists"

# Step 2: Package Lambda function
echo "Step 2: Packaging Lambda function..."
cd backend
zip -r ../lambda-function.zip . -x "*.pyc" -x "__pycache__/*"
cd ..

# Step 3: Upload Lambda package to S3
echo "Step 3: Uploading Lambda package..."
aws s3 cp lambda-function.zip s3://$DEPLOY_BUCKET/lambda-function.zip

# Step 4: Deploy CloudFormation stack
echo "Step 4: Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file template.yaml \
    --stack-name $STACK_NAME \
    --capabilities CAPABILITY_IAM \
    --region $AWS_REGION \
    --parameter-overrides \
        PokemonTCGApiKey=${POKEMON_TCG_API_KEY:-demo-key}

# Step 5: Get outputs
echo ""
echo "Step 5: Getting deployment outputs..."
API_URL=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $AWS_REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
    --output text)

FRONTEND_BUCKET="pokemon-tcg-analyst-${ACCOUNT_ID}"

echo ""
echo "✅ Backend deployed!"
echo "   API URL: $API_URL"
echo ""

# Step 6: Build and deploy frontend
echo "Step 6: Building frontend..."
cd frontend
npm install
REACT_APP_API_URL=$API_URL npm run build
cd ..

echo "Step 7: Deploying frontend to S3..."
aws s3 sync frontend/build/ s3://$FRONTEND_BUCKET/ --delete

FRONTEND_URL="http://${FRONTEND_BUCKET}.s3-website-${AWS_REGION}.amazonaws.com"

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Frontend: $FRONTEND_URL"
echo "API: $API_URL"
echo ""
echo "🎮 Test your application:"
echo "1. Open: $FRONTEND_URL"
echo "2. Select '151' from dropdown"
echo "3. Enter '151 Booster Box'"
echo "4. Click 'Analyze Product'"
echo ""
