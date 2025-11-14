#!/bin/bash
# Diagnose GitHub Actions failure and provide fixes

echo "🔍 Diagnosing GitHub Actions Failure..."
echo "========================================"
echo ""

# Check if gh CLI is available
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI available"
    echo ""
    echo "Fetching latest workflow run..."
    gh run list --repo Camcoder1/pokeAI --limit 1
    echo ""
    echo "Fetching failure logs..."
    gh run view --repo Camcoder1/pokeAI --log-failed
else
    echo "⚠️  GitHub CLI not installed"
    echo ""
    echo "Please check the failure at:"
    echo "https://github.com/Camcoder1/pokeAI/actions"
    echo ""
    echo "Common failure reasons and fixes:"
    echo ""
    echo "1. AWS Credentials Issue"
    echo "   - Verify GitHub Secrets are set correctly"
    echo "   - Check: https://github.com/Camcoder1/pokeAI/settings/secrets/actions"
    echo ""
    echo "2. SAM Build Failed"
    echo "   - Python dependencies issue"
    echo "   - Fix: Check backend/requirements.txt"
    echo ""
    echo "3. CloudFormation Error"
    echo "   - Stack already exists"
    echo "   - Fix: Delete stack: aws cloudformation delete-stack --stack-name pokemon-tcg-analyst"
    echo ""
    echo "4. IAM Permissions"
    echo "   - AWS user lacks permissions"
    echo "   - Fix: Add CloudFormation, Lambda, DynamoDB, S3, API Gateway permissions"
    echo ""
fi

echo "========================================"
echo ""
echo "💡 Next steps:"
echo "1. Check the error in GitHub Actions"
echo "2. Apply the fix above"
echo "3. Or deploy manually: ./deploy.sh"
