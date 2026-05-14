# AI-Powered Recon Framework

An advanced cybersecurity reconnaissance framework built with Python.

This project automates reconnaissance workflows including:

- DNS enumeration
- HTTP fingerprinting
- Port scanning
- SSL analysis
- Subdomain discovery
- Web crawling
- JavaScript endpoint extraction
- Technology fingerprinting
- AI-generated security analysis
- Automated reporting
- Screenshot collection

---

# Features

## Reconnaissance
- Async port scanning
- DNS lookups
- WHOIS analysis
- HTTP probing
- Security header analysis
- SSL certificate inspection

## Web Analysis
- Endpoint crawling
- JavaScript analysis
- Hidden API discovery
- Technology fingerprinting

## AI Features
- Risk scoring
- AI-generated findings
- Security recommendations

## Reporting
- JSON reports
- Markdown reports
- HTML reports
- Screenshot artifacts

---

# Project Structure

```bash
ai-recon-framework/
│
├── ai/
├── core/
├── output/
├── utils/
├── config/
├── tests/
├── main.py
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/JTM-Al555/ai-recon-framework.git
```

## Enter Project

```bash
cd ai-recon-framework
```

## Create Virtual Environment

### Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Install Playwright

```bash
playwright install
```

---

# Usage

```bash
python main.py
```

Enter a target domain:

```bash
chatgpt.com
```

---

# Generated Reports

Reports are automatically saved inside:

```bash
output/
```

Including:
- HTML reports
- Markdown reports
- JSON reports
- Screenshots

---

# Example Features

## Screenshot Collection
Automatically captures screenshots of discovered pages.

## JavaScript Analysis
Extracts hidden endpoints and API paths from JS files.

## AI Analysis
Generates automated security summaries and recommendations.

---

# Security Disclaimer

This tool is for:
- educational purposes,
- authorized testing,
- research environments only.

Do NOT use against systems without permission.

---

# Future Improvements

- FastAPI dashboard
- Docker support
- Shodan integration
- NVD CVE integration
- PDF reporting
- Plugin system
- Distributed scanning

---

# License

MIT License