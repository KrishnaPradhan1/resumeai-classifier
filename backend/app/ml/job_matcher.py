import json
import logging
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline, AutoTokenizer, AutoModel
import torch
import httpx
from aif360.datasets import StandardDataset
from aif360.algorithms.preprocessing import Reweighing
from aif360.metrics import ClassificationMetric
import shap
import lime
from lime.lime_text import LimeTextExplainer
from app.core.config import settings

logger = logging.getLogger(__name__)

class JobMatcherAI:
    """Advanced AI-powered job-resume matching with bias mitigation and explainability"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize BERT for semantic matching
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModel.from_pretrained("bert-base-uncased")
        self.model.to(self.device)
        
        # Initialize TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Initialize text classification for job categorization
        self.job_classifier = pipeline(
            "text-classification",
            model="bert-base-uncased",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Initialize LIME explainer
        self.lime_explainer = LimeTextExplainer(class_names=['Low Match', 'Medium Match', 'High Match'])
        
        logger.info("JobMatcherAI initialized successfully")
    
    async def match_resume_to_job(
        self, 
        resume_data: Dict[str, Any], 
        job_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Match resume to job with comprehensive scoring and explanations"""
        try:
            # Extract features
            resume_features = await self._extract_resume_features(resume_data)
            job_features = await self._extract_job_features(job_data)
            
            # Calculate similarity scores
            similarity_scores = await self._calculate_similarity_scores(
                resume_features, job_features
            )
            
            # Apply bias mitigation
            bias_mitigated_scores = await self._apply_bias_mitigation(
                similarity_scores, resume_data, job_data
            )
            
            # Generate explanations
            explanations = await self._generate_explanations(
                resume_data, job_data, bias_mitigated_scores
            )
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(bias_mitigated_scores)
            
            # Generate match insights
            insights = await self._generate_match_insights(
                resume_data, job_data, bias_mitigated_scores
            )
            
            return {
                "overall_score": overall_score,
                "skills_score": bias_mitigated_scores.get("skills", 0),
                "experience_score": bias_mitigated_scores.get("experience", 0),
                "education_score": bias_mitigated_scores.get("education", 0),
                "culture_score": bias_mitigated_scores.get("culture", 0),
                "skill_matches": insights.get("skill_matches", []),
                "missing_skills": insights.get("missing_skills", []),
                "experience_gap": insights.get("experience_gap", 0),
                "match_explanation": explanations.get("overall", ""),
                "strengths": insights.get("strengths", []),
                "weaknesses": insights.get("weaknesses", []),
                "recommendations": insights.get("recommendations", []),
                "bias_score": bias_mitigated_scores.get("bias_score", 0),
                "fairness_adjustment": bias_mitigated_scores.get("fairness_adjustment", 0),
                "detailed_scores": bias_mitigated_scores,
                "explanations": explanations
            }
            
        except Exception as e:
            logger.error(f"Error matching resume to job: {str(e)}")
            raise
    
    async def _extract_resume_features(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from resume data"""
        try:
            # Extract text content
            resume_text = resume_data.get("extracted_text", "")
            skills = resume_data.get("skills", [])
            experience = resume_data.get("work_experience", [])
            education = resume_data.get("education", [])
            
            # Create feature vectors
            features = {
                "text": resume_text,
                "skills": " ".join(skills),
                "experience_text": " ".join([str(exp) for exp in experience]),
                "education_text": " ".join([str(edu) for edu in education]),
                "skills_list": skills,
                "experience_years": resume_data.get("experience_years", 0),
                "education_level": self._extract_education_level(education)
            }
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting resume features: {str(e)}")
            raise
    
    async def _extract_job_features(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from job data"""
        try:
            # Extract text content
            job_text = job_data.get("description", "")
            required_skills = job_data.get("required_skills", [])
            preferred_skills = job_data.get("preferred_skills", [])
            requirements = job_data.get("requirements", [])
            
            # Create feature vectors
            features = {
                "text": job_text,
                "required_skills": " ".join(required_skills),
                "preferred_skills": " ".join(preferred_skills),
                "requirements_text": " ".join(requirements),
                "all_skills": required_skills + preferred_skills,
                "min_experience": job_data.get("min_experience_years", 0),
                "education_level": job_data.get("education_level", "bachelor")
            }
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting job features: {str(e)}")
            raise
    
    async def _calculate_similarity_scores(
        self, 
        resume_features: Dict[str, Any], 
        job_features: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate similarity scores between resume and job"""
        try:
            scores = {}
            
            # Skills similarity
            skills_similarity = await self._calculate_skills_similarity(
                resume_features["skills_list"], 
                job_features["all_skills"]
            )
            scores["skills"] = skills_similarity
            
            # Experience similarity
            experience_similarity = await self._calculate_experience_similarity(
                resume_features["experience_years"],
                job_features["min_experience"]
            )
            scores["experience"] = experience_similarity
            
            # Education similarity
            education_similarity = await self._calculate_education_similarity(
                resume_features["education_level"],
                job_features["education_level"]
            )
            scores["education"] = education_similarity
            
            # Text similarity using BERT
            text_similarity = await self._calculate_text_similarity(
                resume_features["text"],
                job_features["text"]
            )
            scores["text"] = text_similarity
            
            # Culture fit (soft skills)
            culture_similarity = await self._calculate_culture_similarity(
                resume_features["text"],
                job_features["text"]
            )
            scores["culture"] = culture_similarity
            
            return scores
            
        except Exception as e:
            logger.error(f"Error calculating similarity scores: {str(e)}")
            raise
    
    async def _calculate_skills_similarity(
        self, 
        resume_skills: List[str], 
        job_skills: List[str]
    ) -> float:
        """Calculate skills similarity score"""
        try:
            if not resume_skills or not job_skills:
                return 0.0
            
            # Normalize skills
            resume_skills_normalized = [skill.lower().strip() for skill in resume_skills]
            job_skills_normalized = [skill.lower().strip() for skill in job_skills]
            
            # Calculate intersection
            matching_skills = set(resume_skills_normalized) & set(job_skills_normalized)
            
            # Calculate Jaccard similarity
            union_skills = set(resume_skills_normalized) | set(job_skills_normalized)
            
            if not union_skills:
                return 0.0
            
            similarity = len(matching_skills) / len(union_skills)
            
            # Boost score for required skills
            required_skills = job_skills_normalized[:len(job_skills_normalized)//2]  # Assume first half are required
            required_matches = matching_skills & set(required_skills)
            if required_skills:
                required_boost = len(required_matches) / len(required_skills)
                similarity = (similarity + required_boost) / 2
            
            return min(similarity, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating skills similarity: {str(e)}")
            return 0.0
    
    async def _calculate_experience_similarity(
        self, 
        resume_years: float, 
        job_min_years: float
    ) -> float:
        """Calculate experience similarity score"""
        try:
            if resume_years >= job_min_years:
                # Candidate meets minimum requirement
                if resume_years <= job_min_years * 1.5:
                    # Optimal range
                    return 1.0
                else:
                    # Overqualified - slight penalty
                    return max(0.7, 1.0 - (resume_years - job_min_years * 1.5) / 10)
            else:
                # Underqualified
                gap = job_min_years - resume_years
                if gap <= 1:
                    return 0.8
                elif gap <= 3:
                    return 0.5
                else:
                    return 0.2
                    
        except Exception as e:
            logger.error(f"Error calculating experience similarity: {str(e)}")
            return 0.0
    
    async def _calculate_education_similarity(
        self, 
        resume_education: str, 
        job_education: str
    ) -> float:
        """Calculate education similarity score"""
        try:
            education_levels = {
                "high school": 1,
                "associate": 2,
                "bachelor": 3,
                "master": 4,
                "phd": 5
            }
            
            resume_level = education_levels.get(resume_education.lower(), 0)
            job_level = education_levels.get(job_education.lower(), 0)
            
            if resume_level >= job_level:
                return 1.0
            else:
                gap = job_level - resume_level
                return max(0.3, 1.0 - gap * 0.2)
                
        except Exception as e:
            logger.error(f"Error calculating education similarity: {str(e)}")
            return 0.0
    
    async def _calculate_text_similarity(self, resume_text: str, job_text: str) -> float:
        """Calculate text similarity using BERT embeddings"""
        try:
            # Tokenize and encode texts
            resume_tokens = self.tokenizer(
                resume_text[:512], 
                padding=True, 
                truncation=True, 
                return_tensors="pt"
            )
            job_tokens = self.tokenizer(
                job_text[:512], 
                padding=True, 
                truncation=True, 
                return_tensors="pt"
            )
            
            # Get embeddings
            with torch.no_grad():
                resume_embeddings = self.model(**resume_tokens).last_hidden_state.mean(dim=1)
                job_embeddings = self.model(**job_tokens).last_hidden_state.mean(dim=1)
            
            # Calculate cosine similarity
            similarity = torch.cosine_similarity(resume_embeddings, job_embeddings).item()
            
            return max(0, similarity)  # Ensure non-negative
            
        except Exception as e:
            logger.error(f"Error calculating text similarity: {str(e)}")
            return 0.0
    
    async def _calculate_culture_similarity(self, resume_text: str, job_text: str) -> float:
        """Calculate culture fit using soft skills analysis"""
        try:
            # Use Grok API for advanced culture analysis
            if settings.GROK_API_KEY:
                return await self._calculate_culture_with_grok(resume_text, job_text)
            else:
                return await self._calculate_culture_basic(resume_text, job_text)
                
        except Exception as e:
            logger.error(f"Error calculating culture similarity: {str(e)}")
            return 0.0
    
    async def _calculate_culture_with_grok(self, resume_text: str, job_text: str) -> float:
        """Calculate culture fit using Grok API"""
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
                                "content": "Analyze the cultural fit between a candidate's resume and a job description. Consider soft skills, work style, and values. Return a JSON with a 'score' field (0-1) and 'reasoning' field."
                            },
                            {
                                "role": "user",
                                "content": f"Resume: {resume_text[:1000]}\n\nJob Description: {job_text[:1000]}"
                            }
                        ],
                        "temperature": 0.3
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    analysis = json.loads(content)
                    return analysis.get("score", 0.5)
                else:
                    logger.warning(f"Grok API failed: {response.status_code}")
                    return await self._calculate_culture_basic(resume_text, job_text)
                    
        except Exception as e:
            logger.warning(f"Grok culture analysis failed: {str(e)}")
            return await self._calculate_culture_basic(resume_text, job_text)
    
    async def _calculate_culture_basic(self, resume_text: str, job_text: str) -> float:
        """Basic culture fit calculation"""
        try:
            # Simple keyword matching for soft skills
            soft_skills = [
                "teamwork", "leadership", "communication", "problem solving",
                "collaboration", "initiative", "adaptability", "creativity",
                "time management", "organization", "attention to detail"
            ]
            
            resume_lower = resume_text.lower()
            job_lower = job_text.lower()
            
            resume_skills = [skill for skill in soft_skills if skill in resume_lower]
            job_skills = [skill for skill in soft_skills if skill in job_lower]
            
            if not job_skills:
                return 0.5  # Neutral if no soft skills mentioned
            
            matching_skills = set(resume_skills) & set(job_skills)
            similarity = len(matching_skills) / len(job_skills)
            
            return min(similarity, 1.0)
            
        except Exception as e:
            logger.error(f"Error in basic culture calculation: {str(e)}")
            return 0.5
    
    async def _apply_bias_mitigation(
        self, 
        scores: Dict[str, float], 
        resume_data: Dict[str, Any], 
        job_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """Apply bias mitigation to scores"""
        try:
            mitigated_scores = scores.copy()
            
            # Extract demographic information (if available)
            candidate_name = resume_data.get("candidate_name", "")
            candidate_location = resume_data.get("candidate_location", "")
            
            # Simple bias detection (in production, use more sophisticated methods)
            bias_score = self._detect_potential_bias(candidate_name, candidate_location)
            
            # Apply fairness adjustment
            fairness_adjustment = max(0, 0.1 - bias_score)  # Reduce bias
            
            # Adjust scores
            for key in mitigated_scores:
                if key != "bias_score":
                    mitigated_scores[key] = min(1.0, mitigated_scores[key] + fairness_adjustment)
            
            mitigated_scores["bias_score"] = bias_score
            mitigated_scores["fairness_adjustment"] = fairness_adjustment
            
            return mitigated_scores
            
        except Exception as e:
            logger.error(f"Error applying bias mitigation: {str(e)}")
            return scores
    
    def _detect_potential_bias(self, name: str, location: str) -> float:
        """Detect potential bias in candidate data"""
        try:
            bias_score = 0.0
            
            # This is a simplified example - in production, use more sophisticated bias detection
            # Consider factors like name origin, location demographics, etc.
            
            # Example: Check for location bias (simplified)
            if location and any(city in location.lower() for city in ["new york", "san francisco", "london"]):
                bias_score += 0.05  # Slight bias towards major cities
            
            return min(bias_score, 0.1)  # Cap at 0.1
            
        except Exception as e:
            logger.error(f"Error detecting bias: {str(e)}")
            return 0.0
    
    async def _generate_explanations(
        self, 
        resume_data: Dict[str, Any], 
        job_data: Dict[str, Any], 
        scores: Dict[str, float]
    ) -> Dict[str, str]:
        """Generate explanations for match scores"""
        try:
            explanations = {}
            
            # Overall explanation
            overall_score = self._calculate_overall_score(scores)
            if overall_score >= 0.8:
                explanations["overall"] = "Excellent match! This candidate has strong alignment with the job requirements."
            elif overall_score >= 0.6:
                explanations["overall"] = "Good match. The candidate meets most requirements with some areas for development."
            elif overall_score >= 0.4:
                explanations["overall"] = "Moderate match. The candidate has some relevant experience but may need additional training."
            else:
                explanations["overall"] = "Limited match. The candidate may not be the best fit for this position."
            
            # Skills explanation
            skills_score = scores.get("skills", 0)
            if skills_score >= 0.8:
                explanations["skills"] = "Strong skill alignment with the job requirements."
            elif skills_score >= 0.5:
                explanations["skills"] = "Partial skill match. Some key skills are present."
            else:
                explanations["skills"] = "Limited skill overlap with job requirements."
            
            # Experience explanation
            experience_score = scores.get("experience", 0)
            if experience_score >= 0.8:
                explanations["experience"] = "Experience level well-suited for the position."
            elif experience_score >= 0.5:
                explanations["experience"] = "Experience level is acceptable with some gaps."
            else:
                explanations["experience"] = "Experience level may be insufficient for the role."
            
            return explanations
            
        except Exception as e:
            logger.error(f"Error generating explanations: {str(e)}")
            return {"overall": "Unable to generate explanation at this time."}
    
    async def _generate_match_insights(
        self, 
        resume_data: Dict[str, Any], 
        job_data: Dict[str, Any], 
        scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """Generate detailed match insights"""
        try:
            insights = {}
            
            # Skill matches and gaps
            resume_skills = set(skill.lower() for skill in resume_data.get("skills", []))
            job_skills = set(skill.lower() for skill in job_data.get("required_skills", []) + job_data.get("preferred_skills", []))
            
            skill_matches = list(resume_skills & job_skills)
            missing_skills = list(job_skills - resume_skills)
            
            insights["skill_matches"] = skill_matches
            insights["missing_skills"] = missing_skills
            
            # Experience gap
            resume_years = resume_data.get("experience_years", 0)
            job_min_years = job_data.get("min_experience_years", 0)
            experience_gap = max(0, job_min_years - resume_years)
            
            insights["experience_gap"] = experience_gap
            
            # Strengths and weaknesses
            strengths = []
            weaknesses = []
            
            if scores.get("skills", 0) >= 0.7:
                strengths.append("Strong technical skills alignment")
            else:
                weaknesses.append("Limited technical skills match")
            
            if scores.get("experience", 0) >= 0.7:
                strengths.append("Adequate experience level")
            else:
                weaknesses.append("May need additional experience")
            
            if scores.get("culture", 0) >= 0.7:
                strengths.append("Good cultural fit indicators")
            else:
                weaknesses.append("Cultural fit may need assessment")
            
            insights["strengths"] = strengths
            insights["weaknesses"] = weaknesses
            
            # Recommendations
            recommendations = []
            
            if missing_skills:
                recommendations.append(f"Consider training in: {', '.join(missing_skills[:3])}")
            
            if experience_gap > 0:
                recommendations.append(f"May need {experience_gap} more years of experience")
            
            if scores.get("culture", 0) < 0.5:
                recommendations.append("Consider cultural fit assessment during interview")
            
            insights["recommendations"] = recommendations
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating match insights: {str(e)}")
            return {}
    
    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """Calculate overall match score"""
        try:
            # Weighted average of different scores
            weights = {
                "skills": 0.35,
                "experience": 0.25,
                "education": 0.15,
                "text": 0.15,
                "culture": 0.10
            }
            
            overall_score = 0.0
            total_weight = 0.0
            
            for key, weight in weights.items():
                if key in scores:
                    overall_score += scores[key] * weight
                    total_weight += weight
            
            if total_weight > 0:
                return overall_score / total_weight
            else:
                return 0.0
                
        except Exception as e:
            logger.error(f"Error calculating overall score: {str(e)}")
            return 0.0
    
    def _extract_education_level(self, education: List[Dict[str, Any]]) -> str:
        """Extract highest education level from education list"""
        try:
            if not education:
                return "bachelor"  # Default
            
            education_levels = {
                "phd": 5,
                "doctorate": 5,
                "master": 4,
                "bachelor": 3,
                "associate": 2,
                "high school": 1
            }
            
            highest_level = "bachelor"
            highest_score = 3
            
            for edu in education:
                degree = edu.get("degree", "").lower()
                for level, score in education_levels.items():
                    if level in degree and score > highest_score:
                        highest_level = level
                        highest_score = score
            
            return highest_level
            
        except Exception as e:
            logger.error(f"Error extracting education level: {str(e)}")
            return "bachelor" 