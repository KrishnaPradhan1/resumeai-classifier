import os
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import PyPDF2
from docx import Document
import spacy
from transformers import pipeline, AutoTokenizer, AutoModel
import torch
from pyresparser import ResumeParser
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

class ResumeParserAI:
    """Advanced AI-powered resume parser with multiple extraction methods"""
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize BERT for text classification
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModel.from_pretrained("bert-base-uncased")
        self.model.to(self.device)
        
        # Initialize text classification pipeline
        self.classifier = pipeline(
            "text-classification",
            model="bert-base-uncased",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Skills extraction pipeline
        self.skills_extractor = pipeline(
            "token-classification",
            model="dslim/bert-base-NER",
            device=0 if torch.cuda.is_available() else -1
        )
        
        logger.info("ResumeParserAI initialized successfully")
    
    async def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """Parse resume file and extract structured data"""
        try:
            # Extract text from file
            text = await self._extract_text(file_path)
            if not text:
                raise ValueError("Could not extract text from resume file")
            
            # Parse with pyresparser
            pyresparser_data = await self._parse_with_pyresparser(file_path)
            
            # Enhanced parsing with NLP
            nlp_data = await self._enhance_with_nlp(text)
            
            # Extract skills with AI
            skills_data = await self._extract_skills_ai(text)
            
            # Extract experience with AI
            experience_data = await self._extract_experience_ai(text)
            
            # Extract education with AI
            education_data = await self._extract_education_ai(text)
            
            # Combine all data
            parsed_data = {
                "candidate_name": pyresparser_data.get("name", nlp_data.get("name")),
                "candidate_email": pyresparser_data.get("email", nlp_data.get("email")),
                "candidate_phone": pyresparser_data.get("mobile_number", nlp_data.get("phone")),
                "candidate_location": pyresparser_data.get("location", nlp_data.get("location")),
                "summary": pyresparser_data.get("summary", nlp_data.get("summary")),
                "skills": skills_data.get("skills", []),
                "experience_years": experience_data.get("total_years", 0),
                "work_experience": experience_data.get("experience", []),
                "education": education_data.get("education", []),
                "certifications": pyresparser_data.get("certifications", []),
                "extracted_text": text,
                "confidence_score": self._calculate_confidence(pyresparser_data, nlp_data),
                "parsed_data": {
                    "pyresparser": pyresparser_data,
                    "nlp": nlp_data,
                    "skills": skills_data,
                    "experience": experience_data,
                    "education": education_data
                }
            }
            
            logger.info(f"Successfully parsed resume: {file_path}")
            return parsed_data
            
        except Exception as e:
            logger.error(f"Error parsing resume {file_path}: {str(e)}")
            raise
    
    async def _extract_text(self, file_path: str) -> str:
        """Extract text from various file formats"""
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.pdf':
            return await self._extract_from_pdf(file_path)
        elif file_path.suffix.lower() in ['.docx', '.doc']:
            return await self._extract_from_docx(file_path)
        elif file_path.suffix.lower() == '.txt':
            return await self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    async def _extract_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
            raise
    
    async def _extract_from_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOCX {file_path}: {str(e)}")
            raise
    
    async def _extract_from_txt(self, file_path: Path) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            logger.error(f"Error extracting text from TXT {file_path}: {str(e)}")
            raise
    
    async def _parse_with_pyresparser(self, file_path: str) -> Dict[str, Any]:
        """Parse resume using pyresparser"""
        try:
            parser = ResumeParser(file_path)
            data = parser.get_extracted_data()
            return data
        except Exception as e:
            logger.warning(f"Pyresparser failed for {file_path}: {str(e)}")
            return {}
    
    async def _enhance_with_nlp(self, text: str) -> Dict[str, Any]:
        """Enhance parsing with spaCy NLP"""
        try:
            doc = self.nlp(text)
            
            # Extract entities
            entities = {}
            for ent in doc.ents:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append(ent.text)
            
            # Extract email
            email = None
            for token in doc:
                if "@" in token.text:
                    email = token.text
                    break
            
            # Extract phone numbers
            phone_patterns = [
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                r'\b\(\d{3}\)\s*\d{3}[-.]?\d{4}\b'
            ]
            import re
            phones = []
            for pattern in phone_patterns:
                phones.extend(re.findall(pattern, text))
            
            return {
                "name": entities.get("PERSON", [None])[0] if entities.get("PERSON") else None,
                "email": email,
                "phone": phones[0] if phones else None,
                "location": entities.get("GPE", [None])[0] if entities.get("GPE") else None,
                "organizations": entities.get("ORG", []),
                "summary": text[:500] + "..." if len(text) > 500 else text
            }
            
        except Exception as e:
            logger.warning(f"NLP enhancement failed: {str(e)}")
            return {}
    
    async def _extract_skills_ai(self, text: str) -> Dict[str, Any]:
        """Extract skills using AI models"""
        try:
            # Common skills database
            common_skills = [
                "Python", "JavaScript", "Java", "C++", "C#", "PHP", "Ruby", "Go", "Rust",
                "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "Spring",
                "Docker", "Kubernetes", "AWS", "Azure", "GCP", "SQL", "MongoDB",
                "PostgreSQL", "MySQL", "Redis", "Elasticsearch", "Git", "Jenkins",
                "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn",
                "Data Analysis", "Data Visualization", "Tableau", "Power BI", "Excel",
                "Agile", "Scrum", "Kanban", "JIRA", "Confluence", "Slack", "Microsoft Office"
            ]
            
            # Extract skills using NER
            ner_results = self.skills_extractor(text)
            
            # Find skills in text
            found_skills = []
            for skill in common_skills:
                if skill.lower() in text.lower():
                    found_skills.append(skill)
            
            # Add NER results
            for result in ner_results:
                if result["entity"] in ["ORG", "PRODUCT"]:
                    found_skills.append(result["word"])
            
            return {
                "skills": list(set(found_skills)),
                "confidence": len(found_skills) / len(common_skills) if common_skills else 0
            }
            
        except Exception as e:
            logger.warning(f"Skills extraction failed: {str(e)}")
            return {"skills": [], "confidence": 0}
    
    async def _extract_experience_ai(self, text: str) -> Dict[str, Any]:
        """Extract work experience using AI"""
        try:
            # Use Grok API for advanced experience extraction
            if settings.GROK_API_KEY:
                return await self._extract_experience_with_grok(text)
            else:
                return await self._extract_experience_basic(text)
                
        except Exception as e:
            logger.warning(f"Experience extraction failed: {str(e)}")
            return {"experience": [], "total_years": 0}
    
    async def _extract_experience_with_grok(self, text: str) -> Dict[str, Any]:
        """Extract experience using Grok API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.GROK_API_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.GROK_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "grok-beta",
                        "messages": [
                            {
                                "role": "system",
                                "content": "Extract work experience from this resume. Return JSON with fields: experience (array of objects with company, title, duration, description), total_years (number)"
                            },
                            {
                                "role": "user",
                                "content": text
                            }
                        ],
                        "temperature": 0.1
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    return json.loads(content)
                else:
                    logger.warning(f"Grok API failed: {response.status_code}")
                    return await self._extract_experience_basic(text)
                    
        except Exception as e:
            logger.warning(f"Grok experience extraction failed: {str(e)}")
            return await self._extract_experience_basic(text)
    
    async def _extract_experience_basic(self, text: str) -> Dict[str, Any]:
        """Basic experience extraction using regex and NLP"""
        import re
        from datetime import datetime
        
        # Simple pattern matching for experience
        experience_patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?experience',
            r'experience:\s*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:years?|yrs?)\s*in\s*(?:the\s*)?field'
        ]
        
        total_years = 0
        for pattern in experience_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                total_years = int(match.group(1))
                break
        
        # Extract company names and titles
        doc = self.nlp(text)
        companies = []
        titles = []
        
        for ent in doc.ents:
            if ent.label_ == "ORG":
                companies.append(ent.text)
            elif ent.label_ == "WORK_OF_ART":
                titles.append(ent.text)
        
        experience = []
        for i, company in enumerate(companies[:5]):  # Limit to 5 most recent
            title = titles[i] if i < len(titles) else "Unknown"
            experience.append({
                "company": company,
                "title": title,
                "duration": "Unknown",
                "description": ""
            })
        
        return {
            "experience": experience,
            "total_years": total_years
        }
    
    async def _extract_education_ai(self, text: str) -> Dict[str, Any]:
        """Extract education information using AI"""
        try:
            # Use Grok API for education extraction
            if settings.GROK_API_KEY:
                return await self._extract_education_with_grok(text)
            else:
                return await self._extract_education_basic(text)
                
        except Exception as e:
            logger.warning(f"Education extraction failed: {str(e)}")
            return {"education": []}
    
    async def _extract_education_with_grok(self, text: str) -> Dict[str, Any]:
        """Extract education using Grok API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.GROK_API_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.GROK_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "grok-beta",
                        "messages": [
                            {
                                "role": "system",
                                "content": "Extract education information from this resume. Return JSON with fields: education (array of objects with institution, degree, field, year)"
                            },
                            {
                                "role": "user",
                                "content": text
                            }
                        ],
                        "temperature": 0.1
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    return json.loads(content)
                else:
                    logger.warning(f"Grok API failed: {response.status_code}")
                    return await self._extract_education_basic(text)
                    
        except Exception as e:
            logger.warning(f"Grok education extraction failed: {str(e)}")
            return await self._extract_education_basic(text)
    
    async def _extract_education_basic(self, text: str) -> Dict[str, Any]:
        """Basic education extraction"""
        import re
        
        # Education keywords
        education_keywords = [
            "Bachelor", "Master", "PhD", "Doctorate", "Associate", "Diploma",
            "University", "College", "School", "Institute", "Academy"
        ]
        
        education = []
        lines = text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword.lower() in line_lower for keyword in education_keywords):
                education.append({
                    "institution": line.strip(),
                    "degree": "Unknown",
                    "field": "Unknown",
                    "year": "Unknown"
                })
        
        return {"education": education}
    
    def _calculate_confidence(self, pyresparser_data: Dict, nlp_data: Dict) -> float:
        """Calculate confidence score for parsing results"""
        confidence = 0.0
        total_checks = 0
        
        # Check if we extracted basic information
        if pyresparser_data.get("name") or nlp_data.get("name"):
            confidence += 0.2
        total_checks += 1
        
        if pyresparser_data.get("email") or nlp_data.get("email"):
            confidence += 0.2
        total_checks += 1
        
        if pyresparser_data.get("mobile_number") or nlp_data.get("phone"):
            confidence += 0.2
        total_checks += 1
        
        if pyresparser_data.get("skills"):
            confidence += 0.2
        total_checks += 1
        
        if pyresparser_data.get("experience"):
            confidence += 0.2
        total_checks += 1
        
        return confidence / total_checks if total_checks > 0 else 0.0 