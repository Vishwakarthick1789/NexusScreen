import os
import json
import asyncio
import heapq
from typing import List, Dict, Any
import logging
from openai import AsyncOpenAI
import random

logger = logging.getLogger(__name__)

# Initialize OpenAI client (handles missing API key for mock demo mode)
api_key = os.environ.get("OPENAI_API_KEY", "")
client = AsyncOpenAI(api_key=api_key) if api_key else None

async def evaluate_resume(job_description: str, resume_text: str, candidate_name: str, extracted_skills: List[str]) -> Dict[str, Any]:
    """
    Calls the LLM to evaluate the resume against the job description.
    Returns a JSON object with Technical_Score, Soft_Skills_Analysis, and Red_Flags.
    """
    if not client:
        # Fallback Mock Logic if no API key is provided
        logger.warning("No OPENAI_API_KEY found. Using mock evaluation.")
        await asyncio.sleep(0.5) # Simulate network delay
        score = random.randint(40, 95)
        # Give a boost if we found a lot of skills
        if len(extracted_skills) > 10:
            score = min(100, score + 10)
            
        return {
            "Technical_Score": score,
            "Soft_Skills_Analysis": "Demonstrates good communication and adaptability based on project history.",
            "Red_Flags": "None" if score > 70 else "Lacks deep experience in required core technologies.",
            "Candidate_Name": candidate_name,
            "Skills_Found": ", ".join(extracted_skills[:5]) + ("..." if len(extracted_skills) > 5 else "")
        }

    prompt = f"""
    You are an expert technical recruiter. Evaluate the following resume against the job description.
    Focus on extracting a rationale of fit.
    
    Job Description:
    {job_description}
    
    Resume of {candidate_name}:
    {resume_text}
    
    Pre-extracted Hard Skills:
    {', '.join(extracted_skills)}
    
    You MUST respond with a raw JSON object (do not wrap in markdown tags like ```json) containing exactly these keys:
    - Technical_Score (integer between 0 and 100)
    - Soft_Skills_Analysis (string, 1-2 sentences)
    - Red_Flags (string, or "None")
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        result = json.loads(content)
        result["Candidate_Name"] = candidate_name
        result["Skills_Found"] = ", ".join(extracted_skills[:5]) + ("..." if len(extracted_skills) > 5 else "")
        return result
    except Exception as e:
        logger.error(f"Error evaluating resume for {candidate_name}: {e}")
        return {
            "Technical_Score": 0,
            "Soft_Skills_Analysis": "Error evaluating",
            "Red_Flags": f"API Error: {str(e)}",
            "Candidate_Name": candidate_name,
            "Skills_Found": ""
        }

class TopKCandidatesHeap:
    """
    Min-Heap to track the Top K candidates efficiently without using O(N) memory 
    for large batches of resumes.
    """
    def __init__(self, k: int):
        self.k = k
        self.heap = [] # Min-heap of (score, unique_id, candidate_data)
        self.counter = 0

    def add_candidate(self, candidate_data: Dict[str, Any]):
        score = candidate_data.get("Technical_Score", 0)
        # Using counter to avoid comparing candidate_data dicts if scores are equal
        entry = (score, self.counter, candidate_data)
        self.counter += 1
        
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, entry)
        else:
            # Push new item and pop the smallest if the new item is larger than the smallest
            heapq.heappushpop(self.heap, entry)

    def get_top_candidates(self) -> List[Dict[str, Any]]:
        """Returns the top candidates sorted by score descending."""
        candidates = [item[2] for item in self.heap]
        candidates.sort(key=lambda x: x.get("Technical_Score", 0), reverse=True)
        return candidates
