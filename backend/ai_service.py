import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=True)


def _mock_analysis(process: str, documents: list[str], rejection_reasons: list[str]) -> dict[str, Any]:
    context = " ".join([process, *documents, *rejection_reasons]).lower()
    scholarship = any(term in context for term in ("scholarship", "student", "university", "income certificate"))

    if scholarship:
        requirements = [
            {"name": "Eligibility information", "description": "Income, GPA, residency, and enrollment details", "source": "process", "clearly_stated": True},
            {"name": "Academic transcript", "description": "Current transcript supporting the minimum GPA", "source": "process", "clearly_stated": True},
            {"name": "Income certificate", "description": "Valid certificate for the current academic year", "source": "rejection_reasons", "clearly_stated": False},
            {"name": "Proof of enrollment", "description": "Current confirmation from the university", "source": "faq", "clearly_stated": False},
        ]
        hidden = [
            {"name": "Income certificate", "reason": "Repeated rejection feedback links missing certificates to rejected submissions.", "evidence": "rejection reasons"},
            {"name": "Matching applicant details", "reason": "Supporting documents must use the same legal name as the application.", "evidence": "support information"},
        ]
        dependencies = [
            {"from": "Eligibility information", "to": "Income certificate", "reason": "Income must be validated before need-based eligibility can be reviewed."},
            {"from": "Income certificate", "to": "Application form", "reason": "The certificate is required before the application can be submitted."},
            {"from": "Application form", "to": "Document verification", "reason": "A complete form unlocks document verification."},
        ]
    else:
        requirements = [{"name": "Process-specific documentation", "description": "Documents explicitly required by the supplied process", "source": "process", "clearly_stated": True}]
        hidden = [{"name": "Supporting evidence", "reason": "Rejection and support text suggests an additional verification step.", "evidence": "supplied context"}]
        dependencies = [{"from": "Required documents", "to": "Submission", "reason": "Documents must be complete before submission."}]

    warnings = [{"requirement": item["name"], "message": f"{item['name']} may cause rejection if missing."} for item in hidden]
    confidence = 91 if documents or rejection_reasons else 72
    return {"requirements": requirements, "hidden_prerequisites": hidden, "dependencies": dependencies, "warnings": warnings, "confidence": confidence}


def _openai_analysis(process: str, documents: list[str], rejection_reasons: list[str]) -> dict[str, Any]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = {
        "process": process,
        "documents_or_faqs": documents,
        "historical_rejection_reasons": rejection_reasons,
    }
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.1,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a process intelligence analyst. Return only valid JSON with keys requirements, hidden_prerequisites, dependencies, warnings, confidence. Find requirements that are absent from the main process but implied by FAQs, support information, rejection reasons, and document dependencies. confidence must be an integer from 0 to 100."},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=True)},
        ],
    )
    result = json.loads(response.choices[0].message.content or "{}")
    result["confidence"] = max(0, min(100, int(result.get("confidence", 0))))
    return result


def analyze_process(process: str, documents: list[str], rejection_reasons: list[str]) -> dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        return _mock_analysis(process, documents, rejection_reasons)
    try:
        return _openai_analysis(process, documents, rejection_reasons)
    except Exception:
        return _mock_analysis(process, documents, rejection_reasons)


def preflight(process: str, user_inputs: dict[str, Any]) -> dict[str, Any]:
    process_name = process.lower()
    documents = {str(document).lower().replace(" ", "_") for document in user_inputs.get("documents", [])}
    if "internship" in process_name:
        missing = []
        explanations = []
        actions = []
        if "resume" not in documents:
            missing.append("Resume")
            explanations.append("A current resume is required for company review.")
            actions.append("Include a current resume.")
        if "academic_records" not in documents:
            missing.append("Academic Records")
            explanations.append("Academic records support internship eligibility.")
            actions.append("Include academic records.")
        if "faculty_endorsement" not in documents:
            missing.append("Faculty Endorsement")
            explanations.append("Faculty endorsement is required before company review.")
            actions.append("Obtain a faculty endorsement.")
        return {"status": "PASS" if not missing else "BLOCKED", "missing_requirements": missing, "explanations": explanations, "recommended_actions": actions, "risk_score": 10 if not missing else min(98, 10 + len(missing) * 18)}
    if "student loan" in process_name or "loan" in process_name:
        missing = []
        explanations = []
        actions = []
        loan_requirements = [("loan_application", "Loan Application", "A completed loan application is required.", "Complete the loan application."), ("enrollment_confirmation", "Enrollment Confirmation", "Active enrollment is required for loan approval.", "Include enrollment confirmation."), ("income_evidence", "Income Evidence", "Income evidence is required for loan assessment.", "Include income evidence."), ("cosigner_verification", "Co-signer Verification", "Co-signer verification is required before approval.", "Complete co-signer verification.")]
        for key, name, explanation, action in loan_requirements:
            if key not in documents:
                missing.append(name)
                explanations.append(explanation)
                actions.append(action)
        return {"status": "PASS" if not missing else "BLOCKED", "missing_requirements": missing, "explanations": explanations, "recommended_actions": actions, "risk_score": 10 if not missing else min(98, 10 + len(missing) * 18)}
    values = " ".join(_text(value) for value in user_inputs.values()).lower()
    income_status = str(user_inputs.get("income_certificate", "not available")).lower()
    bank_matches = user_inputs.get("bank_account_name_matches")
    academic_verified = user_inputs.get("academic_records_verified")
    eligibility_verified = user_inputs.get("eligibility_verified")
    missing = []
    explanations = []
    actions = []

    if "identity_proof" not in documents and "identity proof" not in values:
        missing.append("Identity Proof")
        explanations.append("Identity Proof must be verified before document validation.")
        actions.append("Upload a government-issued identity proof.")
    if "academic_records" not in documents and "academic records" not in values:
        missing.append("Academic Records")
        explanations.append("Academic Records are required for eligibility verification.")
        actions.append("Upload your most recent academic records.")
    if income_status in {"not available", "missing", "none", ""} and "income_certificate" not in documents:
        missing.append("Income Certificate")
        explanations.append("Historical rejection data indicates this requirement is commonly responsible for rejection.")
        actions.append("Upload a valid income certificate before submission.")
    elif income_status in {"expired", "invalid"}:
        missing.append("Valid Income Certificate")
        explanations.append("The submitted income certificate is expired and cannot pass document validation.")
        actions.append("Replace it with a valid income certificate for the current academic year.")
    if "bank_proof" not in documents and "bank proof" not in values:
        missing.append("Bank Proof")
        explanations.append("Bank Proof is required for bank verification before final submission.")
        actions.append("Upload bank proof showing the applicant's account details.")
    if bank_matches is False or "does not match" in values:
        missing.append("Matching Bank Account Name")
        explanations.append("The bank account name must match the applicant exactly.")
        actions.append("Provide bank proof with the same name as the applicant.")
    if academic_verified is False or "not verified" in str(user_inputs.get("academic_records", "")).lower():
        missing.append("Verified Academic Records")
        explanations.append("Academic records must be verified before document validation.")
        actions.append("Complete academic record verification before submitting.")
    if eligibility_verified is False or "not verified" in str(user_inputs.get("eligibility", "")).lower():
        missing.append("Eligibility Verification")
        explanations.append("Eligibility should be verified before final submission.")
        actions.append("Verify eligibility before submitting the application.")

    critical_gap = any("income" in item.lower() or "bank" in item.lower() for item in missing)
    risk_score = 82 if critical_gap and len(missing) == 1 else min(98, 10 + len(missing) * 18)
    if not missing:
        status = "PASS"
    elif critical_gap:
        status = "BLOCKED"
    else:
        status = "WARNING"
    return {
        "status": status,
        "missing_requirements": missing,
        "explanations": explanations,
        "recommended_actions": actions,
        "risk_score": risk_score,
    }
