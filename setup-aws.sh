#!/bin/bash
# Initial AWS setup script
# This configures AWS credentials and installs required tools

set -e

echo "🔧 Pokemon TCG Analyst - AWS Setup"
echo "===================================="

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "   https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Check if SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo "❌ AWS SAM CLI not found. Please install it first:"
    echo "   https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html"
    exit 1
fi

echo "✅ AWS CLI found: $(aws --version)"
echo "✅ SAM CLI found: $(sam --version)"
echo ""

# Configure AWS credentials
echo "📋 Configuring AWS credentials..."
read -p "Enter AWS Access Key ID: " AWS_ACCESS_KEY_ID
read -s -p "Enter AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY
echo ""
read -p "Enter AWS Region (default: us-east-1): " AWS_REGION
AWS_REGION=${AWS_REGION:-us-east-1}

aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
aws configure set region "$AWS_REGION"

echo "✅ AWS credentials configured!"

# Verify credentials
echo "🔍 Verifying credentials..."
if aws sts get-caller-identity > /dev/null 2>&1; then
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    echo "✅ Successfully authenticated!"
    echo "   Account ID: $ACCOUNT_ID"
    echo "   Region: $AWS_REGION"
else
    echo "❌ Failed to verify credentials. Please check and try again."
    exit 1
fi

# Optional: Set Pokemon TCG API key
echo ""
read -p "Do you have a Pokemon TCG API key? (y/n): " HAS_API_KEY
if [ "$HAS_API_KEY" = "y" ]; then
    read -p "Enter Pokemon TCG API key: " POKEMON_TCG_API_KEY
    echo "export POKEMON_TCG_API_KEY=\"$POKEMON_TCG_API_KEY\"" >> .env
    echo "✅ Pokemon TCG API key saved to .env"
else
    echo "⚠️  Using demo API key (rate limited). Get a free key at https://pokemontcg.io"
fi

echo ""
echo "✅ Setup complete! You can now run:"
echo "   ./deploy.sh          - Deploy to AWS"
echo "   ./local-test.sh      - Test locally"
echo ""
