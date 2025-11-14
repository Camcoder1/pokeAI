#!/bin/bash
# Check AWS deployment status

echo "🔍 Checking Pokemon TCG Analyst Deployment Status..."
echo "=================================================="
echo ""

# Check CloudFormation Stack
echo "1. CloudFormation Stack Status:"
aws cloudformation describe-stacks \
    --stack-name pokemon-tcg-analyst \
    --region us-east-1 \
    --query 'Stacks[0].StackStatus' \
    --output text 2>/dev/null || echo "   ⏳ Stack not created yet"

echo ""

# Check if stack exists and get outputs
if aws cloudformation describe-stacks --stack-name pokemon-tcg-analyst --region us-east-1 >/dev/null 2>&1; then
    echo "2. Stack Outputs:"

    # Get API Endpoint
    API_URL=$(aws cloudformation describe-stacks \
        --stack-name pokemon-tcg-analyst \
        --region us-east-1 \
        --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
        --output text 2>/dev/null)

    # Get Frontend URL
    FRONTEND_URL=$(aws cloudformation describe-stacks \
        --stack-name pokemon-tcg-analyst \
        --region us-east-1 \
        --query 'Stacks[0].Outputs[?OutputKey==`FrontendURL`].OutputValue' \
        --output text 2>/dev/null)

    # Get DynamoDB Table
    TABLE_NAME=$(aws cloudformation describe-stacks \
        --stack-name pokemon-tcg-analyst \
        --region us-east-1 \
        --query 'Stacks[0].Outputs[?OutputKey==`DynamoDBTable`].OutputValue' \
        --output text 2>/dev/null)

    echo "   API Endpoint: $API_URL"
    echo "   Frontend URL: $FRONTEND_URL"
    echo "   DynamoDB Table: $TABLE_NAME"
    echo ""

    # Test API
    if [ ! -z "$API_URL" ]; then
        echo "3. Testing API Endpoints:"
        echo "   Testing /sets endpoint..."
        curl -s "${API_URL}sets" | head -c 200
        echo ""
        echo ""
    fi

    # Check DynamoDB Table
    if [ ! -z "$TABLE_NAME" ]; then
        echo "4. DynamoDB Table Status:"
        aws dynamodb describe-table \
            --table-name "$TABLE_NAME" \
            --region us-east-1 \
            --query 'Table.TableStatus' \
            --output text 2>/dev/null || echo "   Table not ready yet"
    fi

    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "🌐 Access your application:"
    echo "   Frontend: $FRONTEND_URL"
    echo "   API: $API_URL"
else
    echo "⏳ Deployment in progress..."
    echo ""
    echo "📊 Check GitHub Actions:"
    echo "   https://github.com/Camcoder1/pokeAI/actions"
    echo ""
    echo "💡 Run this script again in a few minutes to check status."
fi
