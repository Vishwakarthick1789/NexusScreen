import re
from typing import List, Set

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.skill_name = None

class SkillTrie:
    def __init__(self, skills: List[str]):
        self.root = TrieNode()
        for skill in skills:
            self.insert(skill)

    def _tokenize(self, text: str) -> List[str]:
        # Simple tokenization: alphanumeric blocks + some symbols like + or # for C++, C#
        return [t.lower() for t in re.findall(r'[a-zA-Z0-9+#.-]+', text)]

    def insert(self, skill: str):
        node = self.root
        tokens = self._tokenize(skill)
        if not tokens:
            return
        for token in tokens:
            if token not in node.children:
                node.children[token] = TrieNode()
            node = node.children[token]
        node.is_end_of_word = True
        node.skill_name = skill

    def extract_skills(self, text: str) -> Set[str]:
        """
        Extracts skills from text in O(L) time where L is the number of tokens in the text,
        assuming the length of skills is bounded.
        """
        tokens = self._tokenize(text)
        found_skills = set()
        n = len(tokens)
        
        for i in range(n):
            node = self.root
            j = i
            while j < n and tokens[j] in node.children:
                node = node.children[tokens[j]]
                if node.is_end_of_word:
                    found_skills.add(node.skill_name)
                j += 1
                
        return found_skills

# Example common tech skills to initialize the Trie
DEFAULT_SKILLS = [
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "React", "Angular",
    "Vue.js", "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring Boot",
    "Ruby on Rails", "Go", "Rust", "PHP", "Laravel", "SQL", "MySQL", "PostgreSQL",
    "MongoDB", "Redis", "Elasticsearch", "AWS", "Azure", "GCP", "Google Cloud",
    "Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins", "Git", "GitHub",
    "GitLab", "CI/CD", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
    "Scikit-Learn", "Pandas", "NumPy", "NLP", "Computer Vision", "Data Science",
    "Data Engineering", "Apache Spark", "Hadoop", "Kafka", "Tableau", "Power BI",
    "PCA", "FAISS", "LLM", "Prompt Engineering", "Agile", "Scrum", "Microservices",
    "REST API", "GraphQL", "Linux", "Bash", "HTML", "CSS", "TailwindCSS", "PyMuPDF"
]
