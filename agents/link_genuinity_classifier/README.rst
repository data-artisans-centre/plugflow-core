# Link Genuinity Classifier Agent

## Overview
This agent provides a comprehensive analysis of URLs to determine their safety and legitimacy.

## Features
- SSL Certificate Validation
- Domain Age Check
- VirusTotal Scanning
- Phishing Pattern Detection
- Comprehensive Risk Scoring

## Installation
1. Install required dependencies:
```bash
pip install pydantic requests python-whois
```

2. Set up API Keys:
- Get a VirusTotal API key from [VirusTotal](https://www.virustotal.com/)
- Configure the key in the agent's configuration

## Usage
```bash
python main.py execute link_genuinity_classifier --params '{"links": ["https://example.com"]}'
```

## Risk Scoring
- 0-50: Likely Safe
- 50-75: Moderate Risk
- 75-100: High Risk

## Contributions
Please submit pull requests or issues to the repository.