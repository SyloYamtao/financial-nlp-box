# 医疗网站项目

一个使用 Next.js 和 Tailwind CSS 构建的现代化、响应式医疗网站，提供全面的医疗服务平台。 
<a href="https://u.geekbang.org/subject/airag/1009927"> 极客时间RAG进阶训练营</a>

学习链接： https://u.geekbang.org/subject/airag/1009927 



![医疗网站首页](frontend/public/images/medical-page.png)


## 功能特点



## 技术栈

- **前端框架**: Next.js
- **样式**: Tailwind CSS
- **图标**: Heroicons
- **动画**: Framer Motion
- **状态管理**: React Context
- **表单处理**: React Hook Form
- **API 集成**: RESTful APIs

## 开始使用

1. 克隆仓库
2. 安装依赖：
   ```bash
   cd frontend
   nvm use v22.14.0
   npm install
   ```
3. 运行开发服务器：
   ```bash
   npm start
   ```
4. 在浏览器中打开 [http://localhost:3000](http://localhost:3000)
5. 后端依赖
```bash
conda create -n rag-project02-medical-nlp-box python=3.11
conda activate rag-project02-medical-nlp-box
pip install -r requirements_mac\(no\ GPU\).txt
```
## 项目结构

```
medical-website/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Navigation.tsx
│   ├── home/
│   │   ├── HeroSection.tsx
│   │   ├── ServiceCategories.tsx
│   │   ├── FeaturedServices.tsx
│   │   ├── WhyChooseUs.tsx
│   │   ├── DoctorProfiles.tsx
│   │   ├── Testimonials.tsx
│   │   └── NewsSection.tsx
│   └── ui/
│       ├── Button.tsx
│       ├── Card.tsx
│       └── Icons.tsx
├── public/
│   └── images/
├── styles/
│   └── globals.css
└── package.json
```

## 参与贡献

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m '添加一些特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情


#### 使用本地下载的 HuggingFace 模型（可选步骤）

* 下载 HuggingFace 模型，以 `BAAI/bge-m3` 为例：

```shell
# 创建 HF_MODEL_PATH 目录
mkdir -p /Users/zhangwufei/hf_model_path
export HF_MODEL_PATH="/Users/zhangwufei/hf_model_path"

cd $HF_MODEL_PATH

# 获取 HuggingFace 模型下载脚本
wget https://hf-mirror.com/hfd/hfd.sh
chmod u+x hfd.sh

# 下载 sentence-transformers/all-MiniLM-L6-v2 模型文件
mkdir -p BAAI/bge-m3
# 建议上午下载，上午网速较快（10MB/s左右）。大概几分钟左右会被限速（近乎停止），可以终止命令，再重新执行，又可以变成高速下载
./hfd.sh BAAI/bge-m3 --tool wget -x 4 -j 1 --local-dir BAAI/bge-m3
```

* 设置 HuggingFace 本地模型文件目录 `HF_MODEL_PATH` 环境变量：

```shell
export HF_MODEL_PATH="/Users/zhangwufei/hf_model_path"
export HF_ENDPOINT=https://hf-mirror.com
```
