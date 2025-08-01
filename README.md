# ResumeAI Classifier

An advanced AI-based resume classification system for recruiters and job portals, leveraging state-of-the-art large language models and machine learning techniques.

## 🚀 Features

- **Advanced Resume Parsing**: Extract structured data from various resume formats (PDF, DOCX, TXT)
- **AI-Powered Matching**: Semantic matching of resumes to job descriptions using LLMs
- **Bias Mitigation**: Fairness algorithms to ensure equitable candidate evaluation
- **Explainable AI**: Insights into why candidates are ranked highly
- **Responsive Design**: Works seamlessly on PCs, laptops, tablets, and mobile devices
- **Real-time Processing**: Fast and efficient resume analysis
- **Secure Deployment**: HTTPS-enabled with advanced security measures

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for modern styling
- **Framer Motion** for advanced animations
- **React Router** for navigation
- **Axios** for API communication

### Backend
- **FastAPI** with Python
- **PostgreSQL** for data storage
- **Redis** for caching
- **Celery** for background tasks
- **JWT** for authentication

### AI/ML
- **Hugging Face Transformers** (BERT, RoBERTa)
- **Grok 3 API** for advanced NLP
- **Pyresparser** for resume parsing
- **SHAP/LIME** for explainability
- **AIF360** for bias mitigation

### Deployment
- **Docker** for containerization
- **Railway/Heroku** for free deployment
- **Cloudflare** for CDN and security

## 📁 Project Structure

```
ResumeAI-Classifier/
├── frontend/                 # React frontend application
├── backend/                  # FastAPI backend application
├── ml_models/               # Machine learning models and scripts
├── docs/                    # Documentation
├── docker-compose.yml       # Docker configuration
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Docker (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ResumeAI-Classifier.git
cd ResumeAI-Classifier
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Environment Configuration**
```bash
# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

5. **Run the Application**
```bash
# Backend (Terminal 1)
cd backend
uvicorn main:app --reload

# Frontend (Terminal 2)
cd frontend
npm start
```

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
DATABASE_URL=postgresql://user:password@localhost/resumeai
REDIS_URL=redis://localhost:6379
GROK_API_KEY=your_grok_api_key
JWT_SECRET=your_jwt_secret
```

**Frontend (.env)**
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GROK_API_KEY=your_grok_api_key
```

## 📊 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh token

### Resume Management
- `POST /resumes/upload` - Upload resume
- `GET /resumes/{id}` - Get resume details
- `GET /resumes/` - List all resumes
- `DELETE /resumes/{id}` - Delete resume

### Job Matching
- `POST /jobs/create` - Create job posting
- `GET /jobs/{id}/matches` - Get matching candidates
- `POST /jobs/{id}/analyze` - Analyze job-resume matches

## 🎨 Features in Detail

### Advanced Frontend
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Smooth Animations**: Framer Motion for engaging user experience
- **Real-time Updates**: WebSocket integration for live updates
- **Dark/Light Mode**: Theme switching capability
- **Progressive Web App**: Offline functionality

### Robust Backend
- **RESTful API**: FastAPI with automatic documentation
- **Database Optimization**: PostgreSQL with proper indexing
- **Caching**: Redis for improved performance
- **Background Tasks**: Celery for heavy processing
- **Security**: JWT authentication, rate limiting, CORS

### AI/ML Capabilities
- **Multi-format Parsing**: PDF, DOCX, TXT support
- **Semantic Matching**: Advanced NLP for job-resume matching
- **Bias Detection**: AIF360 for fairness evaluation
- **Explainability**: SHAP/LIME for transparent decisions
- **Scalable Processing**: Async processing for large volumes

## 🔒 Security Features

- **HTTPS Enforcement**: Secure communication
- **JWT Authentication**: Stateless authentication
- **Rate Limiting**: Prevent abuse
- **Input Validation**: Sanitize all inputs
- **CORS Configuration**: Cross-origin security
- **Environment Variables**: Secure configuration management

## 📱 Device Compatibility

- **Desktop**: Full feature access with advanced UI
- **Laptop**: Optimized for productivity
- **Tablet**: Touch-friendly interface
- **Mobile**: Responsive design with mobile-specific features

## 🚀 Deployment

### Free Deployment Options

1. **Railway** (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy backend
cd backend
railway login
railway up

# Deploy frontend
cd frontend
railway up
```

2. **Heroku**
```bash
# Backend
heroku create resumeai-backend
git push heroku main

# Frontend
heroku create resumeai-frontend
git push heroku main
```

3. **Vercel** (Frontend only)
```bash
npm install -g vercel
vercel --prod
```

## 📈 Performance Optimization

- **CDN Integration**: Cloudflare for global content delivery
- **Image Optimization**: WebP format with fallbacks
- **Code Splitting**: Lazy loading for better performance
- **Database Indexing**: Optimized queries
- **Caching Strategy**: Multi-level caching

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Hugging Face for transformer models
- xAI for Grok 3 API
- FastAPI community for the excellent framework
- React team for the amazing frontend library

## 📞 Support

For support, email support@resumeai.com or create an issue in this repository.

---

**Built with ❤️ for the recruitment industry** 