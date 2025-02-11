# App Magic AI
> AI-powered Smart App Generator

Create complete applications using natural language descriptions, just like magic.

## ✨ Features

- 🪄 Instant App Creation
  > Generate applications in seconds, saving 90% development time
- 🎯 Natural Language to Code
  > Generate complete applications from natural language descriptions
- 🔄 Continuous Evolution
  > Continuous application optimization, automatically adapting to new requirements
- 👥 Team Efficiency
  > Boost team collaboration efficiency by 300%
- 💡 Smart Suggestions
  > Intelligent code suggestions to accelerate development
- 🛡️ Enterprise Ready
  > Enterprise-grade security, ready for immediate deployment
- 📊 Visual Management
  > Visual project management, intuitive and efficient
- 🔍 Code Quality Assurance
  > Automated code review ensuring code quality
- 🚀 Quick Deployment
  > One-click deployment for rapid implementation

## 🎮 Example Applications

### 🌟 Intelligent Chatbot
Generate LLM-powered chat applications with features like:
- Multi-model LLM support (GPT-4, Claude, etc.)
- Real-time conversation
- Context management
- Custom knowledge base integration

### 🌟 E-commerce Platform
Create full-featured online stores including:
- Shopping cart system
- Payment integration
- Order management
- Inventory tracking
- User reviews

### 🌟 Enterprise Management System
Automatically generate enterprise modules such as:
- CRM (Customer Relationship Management)
- ERP (Enterprise Resource Planning)
- HRM (Human Resource Management)
- Project management
- Analytics dashboard

## 🚀 Quick Start

<<<<<<< HEAD
=======
### Windows Prerequisites

1. Install WSL2 (Windows Subsystem for Linux)
```powershell
wsl --install
```

2. Install Docker Desktop for Windows
- Download from [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Ensure WSL2 integration is enabled in Docker Desktop settings

3. Install Git for Windows
- Download from [Git](https://git-scm.com/download/win)

>>>>>>> 848dedb (feat: initial commit with deepseek support)
### Using Docker

1. Clone the repository
```bash
git clone https://github.com/AppMagic-AI/app-magic.git
cd app-magic
```

2. Set up environment variables

Create `backend/.env`:
```bash
DATABASE_URL=postgresql://user:password@db:5432/dbname
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
DEEPSEEK_API_KEY=your-deepseek-api-key
DEFAULT_LLM_MODEL=deepseek-coder-33b-instruct  # or gpt-4-turbo-preview
```

Create `frontend/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Start the application
```bash
docker-compose up -d
```

4. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🛠️ Development Guide

<<<<<<< HEAD
=======
### Windows Development Setup

1. Backend Setup
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn main:app --reload
```

2. Frontend Setup
```powershell
# Install dependencies
npm install

# Start development server
npm run dev
```

3. Database Setup
- Install PostgreSQL for Windows from [official website](https://www.postgresql.org/download/windows/)
- Or use Docker:
```powershell
docker-compose up db
```

>>>>>>> 848dedb (feat: initial commit with deepseek support)
### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# For Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

<<<<<<< HEAD
=======
### Troubleshooting on Windows

1. Port conflicts:
```powershell
# Check if ports are in use
netstat -ano | findstr "3000"
netstat -ano | findstr "8000"

# Kill process by PID
taskkill /PID <process_id> /F
```

2. Python venv issues:
```powershell
# If activation is blocked
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. Docker issues:
- Ensure Hyper-V is enabled
- Verify WSL2 is properly installed
- Restart Docker Desktop

>>>>>>> 848dedb (feat: initial commit with deepseek support)
## 📁 Project Structure
```
app-magic/
├── backend/                 # Backend code
│   ├── alembic/            # Database migrations
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   └── main.py            # Main application
├── frontend/               # Frontend code
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Page components
│   │   └── utils/        # Utility functions
│   └── public/           # Static assets
└── docker-compose.yml    # Docker configuration
```
## 🔨 Usage

<<<<<<< HEAD
## 🔨 Usage

1. Register an account
2. Login to the system
3. Create a new project:
   - Describe your requirements
   - Select project type
   - Click "Generate Project"
4. View and modify code
5. Create versions
6. Add comments

## 🔧 Troubleshooting

### Common Issues

1. Database Connection Errors:
   - Check PostgreSQL service
   - Verify credentials

2. API Errors:
   - Verify API key
   - Check usage limits

3. CORS Issues:
   - Check API URL
   - Verify CORS settings

## 📝 Contributing Guide

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

=======
1. Register an account
2. Login to the system
3. Create a new project:
   - Describe your requirements
   - Select project type
   - Click "Generate Project"
4. View and modify code
5. Create versions
6. Add comments

## 🔧 Troubleshooting

### Common Issues

1. Database Connection Errors:
   - Check PostgreSQL service
   - Verify credentials

2. API Errors:
   - Verify API key
   - Check usage limits

3. CORS Issues:
   - Check API URL
   - Verify CORS settings

## 📝 Contributing Guide

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

>>>>>>> 848dedb (feat: initial commit with deepseek support)
## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI - Backend Framework
- Next.js - Frontend Framework
- OpenAI - AI Support
- All open source libraries
