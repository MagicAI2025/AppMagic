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

Choose one of the following installation methods:

- [Windows Installation Guide](#windows-installation-guide)
- [Linux Installation Guide](#linux-installation-guide)  
- [Docker Installation Guide](#docker-installation-guide)

### Windows Installation Guide

1. Install Required Software
- Python 3.9+ (https://www.python.org/downloads/)
  * Check "Add Python to PATH" during installation
- Node.js 16+ LTS (https://nodejs.org/)
- MySQL (https://dev.mysql.com/downloads/installer/)
  * Remember the database username and password
- Git (https://git-scm.com/download/win)

2. Clone Project
```bash
git clone https://github.com/MagicAI2025/AppMagic.git
cd AppMagic
```

3. Setup Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

4. Configure Database
- Open MySQL command line tool
```sql
CREATE DATABASE appmagic CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. Create Backend Environment Configuration
Create .env file in backend directory:
```env
DATABASE_URL=mysql+pymysql://user:password@db:3306/appmagic
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
DEFAULT_LLM_MODEL=deepseek-coder-33b-instruct
HOST=0.0.0.0
PORT=80
DEBUG=True
```

6. Run Database Migration
```bash
# In backend directory
alembic upgrade head
```

7. Start Backend Service
```bash
# In backend directory
uvicorn main:app --reload
```

8. Setup Frontend
```bash
# Open a new terminal
cd frontend
npm install
```

9. Create Frontend Environment Configuration
Create .env.local in frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:80
```

10. Start Frontend Service
```bash
npm run dev
```

11. Access Application
- Frontend: http://localhost:3000
- API Documentation: http://localhost:80/docs

### Linux Installation Guide

1. Install Required Software
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.9 python3.9-venv nodejs npm mysql-server git

# CentOS/RHEL
sudo dnf install python39 nodejs mysql-server git
sudo systemctl start mysqld
sudo systemctl enable mysqld
```

2. Clone Project
```bash
git clone https://github.com/MagicAI2025/AppMagic.git
cd AppMagic
```

3. Setup Backend
```bash
cd backend
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Configure Database
```bash
sudo mysql
```
```sql
CREATE DATABASE appmagic;
CREATE USER 'appmagic'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON appmagic.* TO 'appmagic'@'localhost';
FLUSH PRIVILEGES;
```

5. Create Backend Environment Configuration
```bash
cp .env.example .env
# Edit .env file to set necessary environment variables
```

6. Run Database Migration and Start Service
```bash
alembic upgrade head
uvicorn main:app --reload
```

7. Setup Frontend
```bash
cd ../frontend
npm install
cp .env.example .env.local
npm run dev
```

### Docker Installation Guide

1. Install Docker and Docker Compose
```bash
# Ubuntu/Debian
sudo apt install docker.io docker-compose

# CentOS/RHEL
sudo dnf install docker docker-compose
```

2. Clone Project
```bash
git clone https://github.com/MagicAI2025/AppMagic.git
cd AppMagic
```

3. Configure Environment Variables
```bash
# Backend configuration
cp backend/.env.example backend/.env
# Edit backend/.env to set necessary environment variables

# Frontend configuration
cp frontend/.env.example frontend/.env.local
```

4. Start Service
```bash
docker-compose up -d
```

5. Access Application
- Frontend: http://localhost:3000
- API Documentation: http://localhost:80/docs

## 🛠️ Development Guide

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
- Install MySQL for Windows from [official website](https://dev.mysql.com/downloads/installer/)
- Or use Docker:
```powershell
docker-compose up db
```

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

### Troubleshooting on Windows

1. Port conflicts:
```powershell
# Check if ports are in use
netstat -ano | findstr "3000"
netstat -ano | findstr "80"

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

### Linux Development Setup

#### Linux Specific Issues

1. Permission Issues
```bash
# Fix directory permissions
sudo chown -R $USER:$USER .
```

2. MySQL Connection Issues
```bash
# Check service status
sudo systemctl status mysql

# View logs
sudo tail -f /var/log/mysql/mysql.log
```

### Docker Development Setup

#### Docker Specific Issues

1. Container Startup Issues
```bash
# Check container status
docker ps -a

# View container logs
docker logs appmagic_backend_1
docker logs appmagic_frontend_1
```

2. Data Persistence Issues
```bash
# View volume information
docker volume ls

# Backup data
docker run --rm -v appmagic_mysql_data:/data -v $(pwd):/backup \
  ubuntu tar cvf /backup/mysql_backup.tar /data
```

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
│   │   └── public/       # Static assets
│   └── docker-compose.yml    # Docker configuration
```