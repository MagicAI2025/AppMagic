# App Magic AI
> AI-powered Smart App Generator | AI驱动的智能应用生成器

Create complete applications using natural language descriptions, just like magic.
像魔法一样，用自然语言描述就能创建完整的应用程序。

## ✨ Features | 特性

- 🪄 Magical App Generation
  > 像魔法一样简单的应用生成
- 🤖 AI-powered Code Generation
  > AI驱动的智能代码生成
- 🎨 Modern React + TypeScript Frontend
  > 现代化的 React + TypeScript 前端
- 🚀 High-performance FastAPI Backend
  > 高性能的 FastAPI 后端
- 🔐 Complete Authentication System
  > 完整的用户认证系统
- 💾 Reliable PostgreSQL Database
  > 可靠的 PostgreSQL 数据库
- 🐳 Easy Docker Deployment
  > 简单的 Docker 部署
- 📝 Code Version Control
  > 代码版本控制
- 💬 Team Collaboration System
  > 团队协作系统

## 🚀 Quick Start | 快速开始

### Using Docker | 使用 Docker

1. Clone the repository | 克隆仓库
```bash
git clone https://github.com/AppMagic-AI/app-magic.git
cd app-magic
```

2. Set up environment variables | 配置环境变量

Create `backend/.env` | 创建后端环境配置:
```bash
DATABASE_URL=postgresql://user:password@db:5432/dbname
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
```

Create `frontend/.env.local` | 创建前端环境配置:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Start the application | 启动应用
```bash
docker-compose up -d
```

4. Access the application | 访问应用
- Frontend | 前端: http://localhost:3000
- Backend API | 后端接口: http://localhost:8000
- API Documentation | 接口文档: http://localhost:8000/docs

## 🛠️ Development | 开发指南

### Backend | 后端开发
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend | 前端开发
```bash
cd frontend
npm install --save-dev @types/react @types/react-dom typescript @types/node
npm install
npm run dev
```

## 📁 Project Structure | 项目结构
```
app-magic/
├── backend/                 # Backend code | 后端代码
│   ├── alembic/            # Database migrations | 数据库迁移
│   ├── models/             # Data models | 数据模型
│   ├── services/           # Business logic | 业务逻辑
│   └── main.py            # Main application | 主应用
├── frontend/               # Frontend code | 前端代码
│   ├── src/
│   │   ├── components/    # React components | React组件
│   │   ├── pages/        # Page components | 页面组件
│   │   └── utils/        # Utility functions | 工具函数
│   └── public/           # Static assets | 静态资源
└── docker-compose.yml    # Docker configuration | Docker配置
```

## 🔨 Usage | 使用方法

1. Register an account | 注册账号
2. Login to the system | 登录系统
3. Create a new project | 创建新项目:
   - Describe your requirements | 描述你的需求
   - Select project type | 选择项目类型
   - Click "Generate Project" | 点击"生成项目"
4. View and modify code | 查看和修改代码
5. Create versions | 创建版本
6. Add comments | 添加评论

## 🔧 Troubleshooting | 故障排除

### Common Issues | 常见问题

1. Database Connection Errors | 数据库连接错误:
   - Check PostgreSQL service | 检查PostgreSQL服务
   - Verify credentials | 验证凭据

2. API Errors | API错误:
   - Verify API key | 验证API密钥
   - Check usage limits | 检查使用限制

3. CORS Issues | 跨域问题:
   - Check API URL | 检查API地址
   - Verify CORS settings | 验证CORS设置

## 📝 Contributing | 贡献指南

1. Fork the repository | Fork仓库
2. Create feature branch | 创建功能分支
3. Commit changes | 提交更改
4. Push to branch | 推送分支
5. Create Pull Request | 创建PR

## 📄 License | 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 Acknowledgments | 致谢

- FastAPI - Backend Framework | 后端框架
- Next.js - Frontend Framework | 前端框架
- OpenAI - AI Support | AI支持
- All open source libraries | 所有开源库