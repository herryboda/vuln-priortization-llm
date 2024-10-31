def suggest_remediation(vuln):
    context = retrieve_context(vuln["description"])
    prompt = f"Suggest remediation for vulnerability {vuln['cve_id']} ... Context: {context}"
    response = Completion.create(model="text-davinci-003", prompt=prompt)
    return response.choices[0].text.strip()
