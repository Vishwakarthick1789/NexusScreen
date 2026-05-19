import os
import subprocess
import sys

def install_fpdf():
    try:
        import fpdf
    except ImportError:
        print("Installing fpdf for mock generation...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf"])

install_fpdf()
from fpdf import FPDF

resumes = {
    "Alice_Backend": "Experienced backend engineer with 5 years of Python, Django, and PostgreSQL. Expert in REST APIs, Docker, and Kubernetes deployment. Built scalable microservices.",
    "Bob_Frontend": "Frontend specialist focusing on React, TypeScript, and TailwindCSS. 4 years of experience building responsive web apps. Familiar with Node.js and GraphQL.",
    "Charlie_Data": "Data Scientist with a background in Machine Learning, Deep Learning, and NLP. Proficient in Python, TensorFlow, PyTorch, Pandas, and Scikit-Learn. Experienced with LLM fine-tuning.",
    "Diana_DevOps": "DevOps engineer with 6 years of experience in AWS, Terraform, Ansible, and Jenkins. Strong Linux and Bash skills. Expert in CI/CD pipelines.",
    "Eve_FullStack": "Full-stack developer with Java, Spring Boot, React, and MySQL. Agile and Scrum practitioner. 3 years of experience in enterprise software development.",
    "Frank_Manager": "Technical Project Manager with experience in Agile, Scrum, and Jira. 10 years of experience managing software teams. Excellent communication skills."
}

os.makedirs("sample_resumes", exist_ok=True)

for name, text in resumes.items():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Resume: {name.replace('_', ' ')}", ln=1, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=text)
    
    path = os.path.join("sample_resumes", f"{name}.pdf")
    pdf.output(path)
    print(f"Generated {path}")

print("\nMock resumes generated successfully in 'sample_resumes' folder.")
