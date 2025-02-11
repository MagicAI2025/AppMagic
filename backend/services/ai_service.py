from openai import OpenAI
import os
from typing import Dict, List, Optional
import json

class AICodeGenerator:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.deepseek_client = OpenAI(
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            base_url=os.getenv('DEEPSEEK_API_BASE', "https://api.deepseek.com/v1")
        )
        self.default_model = os.getenv('DEFAULT_LLM_MODEL', "gpt-4-turbo-preview")

    async def analyze_requirements(self, description: str, model: Optional[str] = None) -> Dict:
        """分析项目需求并生成项目结构"""
        # Select model based on configuration or parameter
        client = self.deepseek_client if (model or self.default_model).startswith('deepseek') else self.openai_client
        model = model or self.default_model
        
        prompt = f"""
        As a professional software architect, please analyze the following project requirements and generate a detailed project structure:

        Requirements:
        {description}

        Please generate:
        1. Project architecture
        2. Technology stack
        3. File structure
        4. Main functional modules
        5. API interface design
        6. Database models

        Return the result in JSON format.
        """

        try:
            response = await client.chat.completions.create(
                model=model,
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
        
        # Select model based on configuration
        client = self.deepseek_client if self.default_model.startswith('deepseek') else self.openai_client
        model = self.default_model
        
        # 生成每个文件的代码
        for file_path in self._get_file_paths(project_structure):
            prompt = f"""
            Generate complete code for {file_path} based on the following project structure:

            Project Structure:
            {json.dumps(project_structure, indent=2)}

            Please generate maintainable code following best practices.
            Include necessary comments and documentation.
            """

            response = await client.chat.completions.create(
                model=model,
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