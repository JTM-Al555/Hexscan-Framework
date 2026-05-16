# HEXSCAN

> AI-Powered Reconnaissance & Attack Surface Mapping Framework

HEXSCAN is an advanced Python-based reconnaissance framework built for security research, attack surface analysis, and authorized defensive assessments.

It combines:
- asynchronous scanning
- web crawling
- JavaScript analysis
- risk scoring
- technology fingerprinting
- AI-powered reporting
- attack surface discovery
- professional reporting

---

# FEATURES

## CORE RECON
- DNS Enumeration
- WHOIS Lookup
- HTTP Probing
- SSL/TLS Analysis
- Async Port Scanning
- Subdomain Enumeration
- Web Crawling
- Directory Discovery
- Parameter Discovery

---

## WEB ANALYSIS
- JavaScript Endpoint Extraction
- Secret Detection
- Security Header Analysis
- Technology Fingerprinting
- WAF Detection

---

## RISK ENGINE
- Risk Scoring
- Severity Classification
- Security Findings
- Attack Surface Analysis

---

## AI FEATURES
- AI-Powered Analysis
- Executive Summary
- Automated Findings Overview

---

## REPORTING
- HTML Reports
- JSON Reports
- Markdown Reports
- PDF Reports
- Scan History Database

---

# INSTALLATION

## Clone Repository + Setup Environment

### Windows

```powershell
git clone https://github.com/JTM-Al555/hexscan.git

cd hexscan

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

---

### Linux / macOS

```bash
git clone https://github.com/JTM-Al555/hexscan.git

cd hexscan

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

---

# USAGE

## Basic Scan

```bash
hexscan example.com
```

---

## Deep Scan

```bash
hexscan example.com --deep
```

---

## Fast Mode

```bash
hexscan example.com --fast
```

---

## Disable JavaScript Analysis

```bash
hexscan example.com --no-js
```

---

## JSON Output

```bash
hexscan example.com --json
```

---

# OUTPUT

HEXSCAN generates reports inside:

```text
output/
```

Generated formats:
- HTML
- JSON
- Markdown
- PDF

---

# PROJECT STRUCTURE

```text
HEXSCAN/
│
├── ai/
│   ├── analyzer.py
│   └── cve_mapper.py
│
├── core/
│   ├── async_scanner.py
│   ├── dir_fuzzer.py
│   ├── dns_enum.py
│   ├── headers_analyzer.py
│   ├── http_probe.py
│   ├── js_analyzer.py
│   ├── parameter_discovery.py
│   ├── risk_engine.py
│   ├── screenshot.py
│   ├── ssl_analyzer.py
│   ├── subdomain_enum.py
│   ├── tech_fingerprint.py
│   ├── waf_detector.py
│   ├── web_crawler.py
│   └── whois_lookup.py
│
├── dashboard/
│   └── app.py
│
├── database/
│   └── database.py
│
├── output/
│
├── utils/
│   ├── banner.py
│   ├── cli.py
│   ├── helpers.py
│   ├── logger.py
│   └── ui.py
│
├── main.py
├── requirements.txt
├── setup.py
└── README.md
```

---

# EXAMPLE FEATURES

## Risk Analysis

```json
{
  "risk_score": 52,
  "risk_level": "High"
}
```

---

## WAF Detection

```json
{
  "detected": true,
  "wafs": [
    "Cloudflare"
  ]
}
```

---

## Directory Discovery

```json
{
  "directories": [
    "/admin",
    "/dashboard",
    "/api"
  ]
}
```

---

# DASHBOARD

Start the dashboard:

```bash
uvicorn dashboard.app:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

---

# DISCLAIMER

HEXSCAN is intended ONLY for:
- authorized security testing
- defensive security research
- educational purposes

Do NOT use this tool against systems you do not own or have explicit permission to assess.

The developer assumes no responsibility for misuse.

---

# ROADMAP

- Advanced Playwright Browser Engine
- Real-Time Dashboard
- Historical Scan Diffing
- Multi-Target Scanning
- Enhanced AI Reporting
- Visual Analytics
- Expanded Secret Detection
- Improved Asset Discovery

---

# LICENSE

MIT License

---

# HEXSCAN

> Professional Reconnaissance Framework for Modern Attack Surface Analysis