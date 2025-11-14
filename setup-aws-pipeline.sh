#!/bin/bash
# Setup AWS CodePipeline for Pokemon TCG Analyst

echo "🚀 Setting up AWS CodePipeline..."
echo "=================================="
echo ""

# Check if GitHub token is provided
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  GitHub Personal Access Token required"
    echo ""
    echo "Create one at: https://github.com/settings/tokens/new"
    echo "Required scopes: repo, admin:repo_hook"
    echo ""
    read -s -p "Enter GitHub Token: " GITHUB_TOKEN
    echo ""
fi

# Check if Pokemon TCG API key is provided
if [ -z "$POKEMON_TCG_API_KEY" ]; then
    echo "⚠️  Pokemon TCG API Key (optional but recommended)"
    echo ""
    read -p "Enter Pokemon TCG API Key (or press Enter for demo): " POKEMON_TCG_API_KEY
    POKEMON_TCG_API_KEY=${POKEMON_TCG_API_KEY:-demo-key}
fi

echo ""
echo "📦 Deploying CodePipeline CloudFormation stack..."

aws cloudformation deploy \
    --stack-name pokemon-tcg-pipeline \
    --template-file aws-pipeline/codepipeline-template.yaml \
    --parameter-overrides \
        GitHubToken=$GITHUB_TOKEN \
        GitHubOwner=Camcoder1 \
        GitHubRepo=pokeAI \
        GitHubBranch=main \
        PokemonTCGApiKey=$POKEMON_TCG_API_KEY \
    --capabilities CAPABILITY_IAM \
    --region us-east-1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ AWS CodePipeline deployed successfully!"
    echo ""

    # Get pipeline URL
    PIPELINE_URL=$(aws cloudformation describe-stacks \
        --stack-name pokemon-tcg-pipeline \
        --query 'Stacks[0].Outputs[?OutputKey==`PipelineUrl`].OutputValue' \
        --output text)

    echo "🌐 Pipeline Console: $PIPELINE_URL"
    echo ""
    echo "💡 Next steps:"
    echo "1. Pipeline will automatically deploy on every git push to main"
    echo "2. Monitor at: $PIPELINE_URL"
    echo "3. First deployment will start automatically now"
    echo ""
    echo "🔄 To manually trigger:"
    echo "   aws codepipeline start-pipeline-execution --name pokemon-tcg-analyst-pipeline"
else
    echo ""
    echo "❌ Deployment failed. Check the error above."
    exit 1
fi
