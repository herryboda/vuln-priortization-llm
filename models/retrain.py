import openai
from db.crud import get_vulnerabilities

def retrain_rag_model(db):
    vulnerabilities = get_vulnerabilities(db)
    embeddings = [Embedding.create(input=vuln.description) for vuln in vulnerabilities]
    vector_db.update(embeddings)
    print("Knowledge base updated with new CVE data.")
