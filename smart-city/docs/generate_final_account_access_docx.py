from datetime import datetime
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import xml.sax.saxutils as saxutils


OUTPUT = Path(__file__).parent / "final-account-access-checklist.docx"


def p(text: str) -> str:
    safe = saxutils.escape(text)
    return f"<w:p><w:r><w:t xml:space=\"preserve\">{safe}</w:t></w:r></w:p>"


title = "Smart City Project - Final Account Access Checklist"
date_line = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}"

lines = [
    title,
    date_line,
    "",
    "Purpose:",
    "This document lists the 3 remaining areas that require actual cloud/account access to finish the capstone completely.",
    "",
    "1) GitHub + Azure Authentication & Deployment Secrets (MANDATORY)",
    "- Add GitHub repository secrets:",
    "  AZURE_CREDENTIALS",
    "  AKS_RG_STAGING",
    "  AKS_CLUSTER_STAGING",
    "  AKS_RG_PROD",
    "  AKS_CLUSTER_PROD",
    "- Create GitHub Environments:",
    "  staging",
    "  production (with required reviewers for approval gate).",
    "- Expected output:",
    "  CI/CD can authenticate to Azure and target both AKS clusters.",
    "",
    "2) Azure Subscription-Level Provisioning (Terraform Apply with Real Credentials)",
    "- Run Terraform with real subscription context to provision:",
    "  Resource Group, VNet/Subnet, AKS, PostgreSQL Flexible Server, Key Vault (optional),",
    "  Log Analytics + Application Insights (optional), Budget alert (optional).",
    "- Required real inputs:",
    "  subscription_id, budget_contact_emails, and proper role permissions.",
    "- Expected output:",
    "  Infrastructure exists in Azure and outputs can be consumed by deployment/runtime.",
    "",
    "3) Runtime Secret Wiring + AKS Release Validation",
    "- Create real Kubernetes secret (smart-city-secrets) with valid DATABASE_URL in cluster.",
    "- Ensure image pull access for registry (GHCR/ACR) from AKS.",
    "- Execute staging deploy, run smoke test, then approve production deploy.",
    "- Validate post-deploy:",
    "  /health, /metrics, /sensors, /alerts, and /metrics/prometheus endpoints.",
    "- Expected output:",
    "  End-to-end production-like workflow is fully operational on cloud infrastructure.",
    "",
    "Definition of Done",
    "- CI/CD run passes through staging and production stages.",
    "- AKS workloads are healthy (pods/services/hpa/ingress).",
    "- API and frontend consume live backend data from cloud deployment.",
    "- Budget and monitoring hooks are visible in Azure portal.",
]

document_xml = (
    "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
    "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" "
    "xmlns:mc=\"http://schemas.openxmlformats.org/markup-compatibility/2006\" "
    "xmlns:o=\"urn:schemas-microsoft-com:office:office\" "
    "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
    "xmlns:m=\"http://schemas.openxmlformats.org/officeDocument/2006/math\" "
    "xmlns:v=\"urn:schemas-microsoft-com:vml\" "
    "xmlns:wp14=\"http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing\" "
    "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
    "xmlns:w10=\"urn:schemas-microsoft-com:office:word\" "
    "xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
    "xmlns:w14=\"http://schemas.microsoft.com/office/word/2010/wordml\" "
    "xmlns:wpg=\"http://schemas.microsoft.com/office/word/2010/wordprocessingGroup\" "
    "xmlns:wpi=\"http://schemas.microsoft.com/office/word/2010/wordprocessingInk\" "
    "xmlns:wne=\"http://schemas.microsoft.com/office/word/2006/wordml\" "
    "xmlns:wps=\"http://schemas.microsoft.com/office/word/2010/wordprocessingShape\" mc:Ignorable=\"w14 wp14\">"
    "<w:body>"
    + "".join(p(line) for line in lines)
    + "<w:sectPr><w:pgSz w:w=\"12240\" w:h=\"15840\"/><w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/></w:sectPr>"
    "</w:body></w:document>"
)

content_types_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>
"""

rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""

with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as docx:
    docx.writestr("[Content_Types].xml", content_types_xml)
    docx.writestr("_rels/.rels", rels_xml)
    docx.writestr("word/document.xml", document_xml)

print(f"Created: {OUTPUT}")
