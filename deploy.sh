#!/bin/bash

# ResumeAI Classifier - Quick Deployment Script
# This script helps you deploy the ResumeAI Classifier to free hosting platforms

set -e

echo "🚀 ResumeAI Classifier - Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if git is installed
check_git() {
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install Git first."
        exit 1
    fi
    print_success "Git is installed"
}

# Check if node is installed
check_node() {
    if ! command -v node &> /dev/null; then
        print_warning "Node.js is not installed. You'll need it for local development."
    else
        print_success "Node.js is installed"
    fi
}

# Check if python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 is not installed. You'll need it for local development."
    else
        print_success "Python 3 is installed"
    fi
}

# Initialize git repository
init_git() {
    print_status "Initializing Git repository..."
    
    if [ ! -d ".git" ]; then
        git init
        print_success "Git repository initialized"
    else
        print_status "Git repository already exists"
    fi
}

# Create .gitignore
create_gitignore() {
    print_status "Creating .gitignore file..."
    
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# Environment Variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# nyc test coverage
.nyc_output

# Dependency directories
node_modules/
jspm_packages/

# Optional npm cache directory
.npm

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env

# next.js build output
.next

# Nuxt.js build output
.nuxt

# Gatsby files
.cache/
public

# Storybook build outputs
.out
.storybook-out

# Temporary folders
tmp/
temp/

# Database
*.db
*.sqlite
*.sqlite3

# Uploads
uploads/
*.pdf
*.docx
*.doc

# ML Models
models/
*.pkl
*.joblib

# Celery
celerybeat-schedule
celerybeat.pid

# Redis
dump.rdb

# Docker
.dockerignore
docker-compose.override.yml
EOF

    print_success ".gitignore file created"
}

# Create environment files
create_env_files() {
    print_status "Creating environment files..."
    
    # Backend .env
    cat > backend/.env.example << EOF
# Database Configuration
DATABASE_URL=postgresql://resumeai:resumeai123@localhost:5432/resumeai
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=false

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,https://your-frontend-domain.vercel.app

# AI/ML APIs
GROK_API_KEY=your-grok-api-key-here

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
EOF

    # Frontend .env
    cat > frontend/.env.example << EOF
# API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GROK_API_KEY=your-grok-api-key-here

# Build Configuration
GENERATE_SOURCEMAP=false
INLINE_RUNTIME_CHUNK=false
EOF

    print_success "Environment files created"
}

# Create deployment status file
create_deployment_status() {
    print_status "Creating deployment status file..."
    
    cat > DEPLOYMENT_STATUS.md << EOF
# Deployment Status

## Backend (Railway)
- [ ] Repository pushed to GitHub
- [ ] Railway project created
- [ ] Environment variables configured
- [ ] PostgreSQL database added
- [ ] Backend deployed successfully
- [ ] Health check passed

## Frontend (Vercel)
- [ ] Vercel project created
- [ ] Environment variables configured
- [ ] Frontend deployed successfully
- [ ] API connection verified

## Configuration
- [ ] CORS settings updated
- [ ] API URL updated in frontend
- [ ] Custom domain configured (optional)
- [ ] SSL certificate verified

## Testing
- [ ] Login/Register functionality
- [ ] Resume upload working
- [ ] Job matching working
- [ ] Mobile responsiveness verified

## Performance
- [ ] Page load times optimized
- [ ] Database queries optimized
- [ ] Caching implemented
- [ ] Error monitoring configured

Last updated: $(date)
EOF

    print_success "Deployment status file created"
}

# Main deployment function
main() {
    echo ""
    print_status "Starting deployment setup..."
    
    # Check prerequisites
    check_git
    check_node
    check_python
    
    # Setup project
    init_git
    create_gitignore
    create_env_files
    create_deployment_status
    
    echo ""
    print_success "Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Create a GitHub repository"
    echo "2. Push your code to GitHub"
    echo "3. Follow the DEPLOYMENT.md guide"
    echo "4. Deploy to Railway (backend) and Vercel (frontend)"
    echo ""
    echo "For detailed instructions, see: DEPLOYMENT.md"
    echo ""
}

# Run main function
main "$@" 