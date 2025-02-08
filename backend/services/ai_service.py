from openai import OpenAI
import os
from typing import Dict, List
import json

class AICodeGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4-turbo-preview"  # 使用最新的 GPT-4 模型

    async def analyze_requirements(self, description: str) -> Dict:
        """分析项目需求并生成项目结构"""
        prompt = f"""
        作为一个专业的软件架构师，请分析以下项目需求并生成详细的项目结构：

        需求描述：
        {description}

        请生成：
        1. 项目架构
        2. 技术栈选择
        3. 文件结构
        4. 主要功能模块
        5. API 接口设计
        6. 数据库模型

        以 JSON 格式返回结果。
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional software architect."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from AI service")
        except Exception as e:
            raise RuntimeError(f"AI service error: {str(e)}")

    async def generate_code(self, project_structure: Dict) -> Dict[str, str]:
        """根据项目结构生成代码"""
        files = {}
        
        # 生成每个文件的代码
        for file_path in self._get_file_paths(project_structure):
            prompt = f"""
            根据以下项目结构生成 {file_path} 的完整代码：

            项目结构：
            {json.dumps(project_structure, indent=2)}

            请生成符合最佳实践的、可维护的代码。
            包含必要的注释和文档字符串。
            """

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional software developer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            files[file_path] = response.choices[0].message.content

        return files

    def _get_file_paths(self, project_structure: Dict) -> List[str]:
        """从项目结构中提取需要生成的文件路径"""
        file_paths = []
        
        # 前端文件
        if 'frontend' in project_structure:
            file_paths.extend([
                'frontend/src/pages/index.tsx',
                'frontend/src/components/Layout.tsx',
                'frontend/src/utils/api.ts',
                'frontend/src/styles/globals.css',
            ])
        
        # 后端文件
        if 'backend' in project_structure:
            file_paths.extend([
                'backend/main.py',
                'backend/models/database.py',
                'backend/services/auth.py',
                'backend/utils/helpers.py',
            ])

        return file_paths

    async def optimize_code(self, code: str, language: str) -> str:
        """优化生成的代码"""
        prompt = f"""
        请优化以下{language}代码，确保：
        1. 代码遵循最佳实践
        2. 性能优化
        3. 安全性考虑
        4. 可维护性提升

        代码：
        {code}
        """

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a code optimization expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )

        return response.choices[0].message.content

    async def generate_tests(self, code: str, language: str) -> str:
        """为生成的代码生成测试用例"""
        prompt = f"""
        请为以下{language}代码生成完整的测试用例：
        1. 单元测试
        2. 集成测试
        3. 边界条件测试

        代码：
        {code}
        """

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a testing expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )

        return response.choices[0].message.content 