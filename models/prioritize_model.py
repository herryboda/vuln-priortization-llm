from openai import Completion, Embeddings
from db.crud import get_user_settings

def prioritize_vulnerabilities(vulnerabilities, user_id, db):
    user_settings = get_user_settings(db, user_id)
    prioritized = []
    for vuln in vulnerabilities:
        context = retrieve_context(vuln["description"])
        prompt = f"Prioritize vulnerability {vuln['cve_id']} ... Context: {context}"
        response = Completion.create(model="text-davinci-003", prompt=prompt)
        base_score = float(response.choices[0].text.strip())
        
        # Customizable weighting factors from user settings
        priority_score = base_score * user_settings.cvss_weight * vuln.cvss_score \
            + user_settings.exploitability_weight * vuln.exploitability \
            + user_settings.reachability_weight * (1 if vuln.reachability else 0)
        prioritized.append({"cve_id": vuln["cve_id"], "priority_score": priority_score})
    prioritized.sort(key=lambda x: x["priority_score"], reverse=True)
    return prioritized

def retrieve_context(description):
    # Retrieve similar vulnerabilities from vector database for context
    vectors = Embeddings.create(input=description)
    context = vector_db.query(vectors)
    return context
