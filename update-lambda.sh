#!/bin/bash
# Quick update to fix Lambda

echo "Creating updated Lambda package..."

cd backend/package
cp ../app.py .

# Create zip
zip -r ../../lambda-update.zip . > /dev/null

cd ../..

echo "Uploading to Lambda..."
aws lambda update-function-code \
    --function-name pokemon-tcg-analyst-PokemonAnalyzerFunction-uf6xnGV7cnon \
    --zip-file fileb://lambda-update.zip \
    --region us-east-1

echo "Waiting for update to complete..."
sleep 5

echo "Testing..."
curl "https://blvkupimh3.execute-api.us-east-1.amazonaws.com/prod/sets"
