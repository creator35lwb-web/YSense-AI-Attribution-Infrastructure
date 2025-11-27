# YSenseAI™ v4.5-Beta: Ethical AI Training Data Platform

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17737995.svg)](https://doi.org/10.5281/zenodo.17737995)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Z-Protocol v2.0](https://img.shields.io/badge/Z--Protocol-v2.0-blue.svg)](https://doi.org/10.5281/zenodo.17072168)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status: Beta](https://img.shields.io/badge/status-beta-orange.svg)]()

**Build your personal wisdom library while contributing to ethical AI development.**

YSenseAI is an open-source platform that enables individuals to share their cultural wisdom, personal reflections, and lived experiences in a way that respects their sovereignty, provides fair compensation, and protects cultural heritage. Built on the Z-Protocol v2.0 framework, it ensures transparent attribution, granular consent management, and ethical AI training data practices.

---

## 📚 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Z-Protocol v2.0](#z-protocol-v20)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Use Cases](#use-cases)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Citation](#citation)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## 🌟 Overview

### The Problem

AI models are trained on vast amounts of data scraped from the internet, often without:
- **Consent** from content creators
- **Attribution** to original sources
- **Compensation** for contributors
- **Cultural sensitivity** for traditional knowledge
- **Quality metrics** for training optimization

This creates ethical, legal, and technical challenges for AI development.

### The Solution

YSenseAI provides a **consent-first, attribution-native platform** where:

1. **Users control their data** through granular consent management (Z-Protocol v2.0)
2. **Creators are compensated** with 15-30% revenue sharing based on content tier
3. **Cultural heritage is protected** with community attribution and benefit sharing
4. **Quality is optimized** with 6 training metrics for AI model performance
5. **Attribution is cryptographic** with SHA-256 fingerprinting and DID assignment

### Core Innovation

**Story-First AI-Native UX**: Users write freely, AI extracts structured wisdom layers, then collaborates with users to distill essence through dialogue. This creates:
- **Rich training data** (5 perception layers + 3-word distillation)
- **User self-discovery** (reflective conversation with AI)
- **Personal knowledge library** (exportable in JSON/MD/CSV)
- **Training-optimized format** (Alpaca, ShareGPT, JSONL)

---

## ✨ Key Features

### For Users

- **📝 Story Canvas**: Write freely about meaningful moments
- **🧠 AI Analysis**: Automatic extraction of 5 perception layers (Narrative, Somatic, Attention, Synesthetic, Temporal)
- **💬 Collaborative Distillation**: Chat with AI to refine 3-word essence
- **🛡️ Z-Protocol Consent**: Choose content tier and AI training consent
- **📚 Personal Library**: Search, view, and manage all submissions
- **📊 Quality Metrics**: See training optimization scores
- **💰 Revenue Tracking**: Estimate earnings from AI training
- **📥 Export Features**: Download in JSON (for personal LLM), Markdown, CSV

### For Developers

- **🔒 Attribution Engine**: Cryptographic signing with SHA-256 + DID
- **📈 Quality Metrics**: 6 training optimization signals
  - Context efficiency (300-800 token sweet spot)
  - Reasoning depth (5-layer CoT)
  - Cultural specificity (>70% unique markers)
  - Emotional richness (>15 descriptors/100 words)
  - Attention density (3+ details/layer)
  - Compression quality (>80% essence preserved)
- **🤝 Consent Management**: 8 consent types with audit trail
- **💾 Database Schema**: SQLite with GDPR-compliant deletion (72 hours)
- **🔌 AI Integration**: Claude (Anthropic) + Qwen (Alibaba Cloud)
- **📦 Export Pipeline**: JSONL, Alpaca, ShareGPT, CSV, Dataset Card

### For AI Labs

- **✅ Legally-safe data**: All content has explicit AI training consent
- **✅ Attributed data**: Cryptographic provenance for every submission
- **✅ High-quality data**: Training-optimized with 6 quality metrics
- **✅ Culturally-rich data**: 5-layer perception analysis
- **✅ Ethically-sourced data**: Z-Protocol v2.0 compliant
- **✅ Training-ready format**: Alpaca, ShareGPT, JSONL

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                      YSenseAI Platform                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Frontend   │    │   Backend    │    │   Database   │  │
│  │  (Streamlit) │───▶│   (Python)   │───▶│   (SQLite)   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                    │                    │          │
│         │                    │                    │          │
│         ▼                    ▼                    ▼          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Story Canvas │    │ AI Agents    │    │ Consent Mgmt │  │
│  │ 5-Layer UI   │    │ Claude+Qwen  │    │ Z-Protocol   │  │
│  │ Collab Chat  │    │ Distillation │    │ 8 Types      │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                    │                    │          │
│         │                    │                    │          │
│         ▼                    ▼                    ▼          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Personal Lib │    │ Attribution  │    │ Quality      │  │
│  │ Search+Export│    │ SHA-256+DID  │    │ 6 Metrics    │  │
│  │ JSON/MD/CSV  │    │ Crypto Sign  │    │ Training Opt │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Export Pipeline  │
                    │  JSONL, Alpaca,   │
                    │  ShareGPT, CSV    │
                    └──────────────────┘
```

### Technology Stack

**Frontend**:
- Streamlit 1.28+ (Python web framework)
- Custom CSS for sanctuary aesthetic
- Responsive design (mobile-friendly)

**Backend**:
- Python 3.11+
- SQLite (production-ready with WAL mode)
- Anthropic Claude API (AI analysis)
- Alibaba Cloud Qwen API (quality metrics)

**Attribution**:
- SHA-256 cryptographic hashing
- DID (Decentralized Identifier) system
- JSON-LD for metadata
- Blockchain-ready architecture

**Consent**:
- Z-Protocol v2.0 framework
- 5-tier classification system
- 8 consent types
- GDPR-compliant (72-hour deletion)

---

## 🛡️ Z-Protocol v2.0

YSenseAI is built on the **Z-Protocol v2.0**, a comprehensive ethical framework for AI attribution and cultural protection.

### Five-Tier Classification

| Tier | Description | Revenue Share | Protection Level |
|------|-------------|---------------|------------------|
| **PUBLIC** | General reflections, non-sensitive | 15% | Standard |
| **PERSONAL** | Individual experiences, family | 20% | Enhanced |
| **CULTURAL** | Traditional knowledge, practices | 25% + fund | Community attribution |
| **SACRED** | Religious, spiritual content | 30% + fund | Restricted access |
| **THERAPEUTIC** | Mental health, trauma | 25% + fund | Medical ethics |

### Eight Consent Types

1. **Account Creation** (Required)
2. **Wisdom Storage** (Required for submissions)
3. **AI Training Contribution** (Optional, Compensated 15-30%)
4. **Community Sharing** (Optional)
5. **Cultural Knowledge Sharing** (Optional, for Cultural/Sacred tiers)
6. **Revenue Sharing** (Automatic with AI training consent)
7. **Research Participation** (Optional, Anonymized)
8. **Anonymized Analytics** (Optional)

### Key Principles

- **Consent-First**: No data use without explicit consent
- **Transparent Attribution**: Cryptographic provenance for all content
- **Fair Compensation**: 15-30% revenue sharing based on tier
- **Cultural Protection**: Community approval for Cultural/Sacred content
- **User Sovereignty**: Full control over data (export, edit, delete)
- **GDPR Compliant**: All user rights implemented

**Learn More**: [Z-Protocol v2.0 Complete Framework](https://doi.org/10.5281/zenodo.17072168)

---

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git
- (Optional) Virtual environment tool (venv, conda)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/YSense-AI-Attribution-Infrastructure.git
cd YSense-AI-Attribution-Infrastructure

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_production.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys (see Configuration section)

# Initialize database
python -c "from v45_beta.database.schema import Database; Database()"

# Run the application
streamlit run v45_beta/app_legal_protected.py
```

### Docker Install

```bash
# Build Docker image
docker build -t ysenseai:v4.5-beta .

# Run container
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY=your_key \
  -e QWEN_API_KEY=your_key \
  ysenseai:v4.5-beta
```

### Configuration

Create a `.env` file with your API keys:

```env
# Anthropic Claude API (required)
ANTHROPIC_API_KEY=sk-ant-api03-...

# Alibaba Cloud Qwen API (required)
QWEN_API_KEY=sk-...
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1

# Database (optional, defaults to SQLite)
DATABASE_PATH=./ysense_production.db

# Security (optional, auto-generated if not set)
JWT_SECRET=your_secret_key_here
```

**Get API Keys**:
- **Claude**: https://console.anthropic.com/
- **Qwen**: https://www.alibabacloud.com/help/en/model-studio/get-api-key

---

## 🎯 Quick Start

### 1. Register an Account

```bash
# Start the application
streamlit run v45_beta/app_legal_protected.py
```

Navigate to `http://localhost:8501` and:
1. Click "Register" tab
2. Read and accept Privacy Policy and Terms of Service
3. Acknowledge beta status
4. Create your account

### 2. Submit Your First Wisdom

1. Click "✨ Submit Wisdom" in sidebar
2. Write a story about a meaningful moment
3. Click "Analyze Story" - AI extracts 5 perception layers
4. Chat with AI to refine the 3-word distillation
5. Choose Z-Protocol tier (Public/Personal/Cultural/Sacred/Therapeutic)
6. Opt-in to AI training (optional, 15-30% revenue share)
7. Click "💾 Save Wisdom"

### 3. View Your Library

1. Click "📚 My Library" in sidebar
2. Search your submissions
3. View quality scores
4. Export individual wisdom (JSON/MD)

### 4. Export Your Data

1. Go to "⚙️ Settings"
2. Click "Export All Data"
3. Choose format (JSON for personal LLM, Markdown for notes, CSV for analysis)
4. Download your complete wisdom library

---

## 📖 Documentation

### For Users

- [User Guide](docs/USER_GUIDE.md) - Complete walkthrough
- [Privacy Policy](v45_beta/legal/privacy_policy.md) - GDPR-compliant privacy notice
- [Terms of Service](v45_beta/legal/terms_of_service.md) - Beta program terms
- [FAQ](docs/FAQ.md) - Frequently asked questions

### For Developers

- [Architecture](docs/ARCHITECTURE.md) - System design and components
- [API Reference](docs/API_REFERENCE.md) - Internal API documentation
- [Database Schema](docs/DATABASE_SCHEMA.md) - SQLite schema and relationships
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community guidelines

### For Researchers

- [Z-Protocol v2.0 Specification](docs/Z_PROTOCOL_V2.md) - Complete framework
- [Quality Metrics](docs/QUALITY_METRICS.md) - Training optimization signals
- [Attribution Engine](docs/ATTRIBUTION_ENGINE.md) - Cryptographic provenance
- [Export Formats](docs/EXPORT_FORMATS.md) - JSONL, Alpaca, ShareGPT

---

## 💡 Use Cases

### 1. Personal Knowledge Management

Build your own wisdom library and export for personal LLM training:

```python
# Export your wisdom for personal LLM
import json

with open('my_wisdom.json', 'r') as f:
    wisdom = json.load(f)

# Use with Llama, Mistral, or any open-source model
# Fine-tune on your personal reflections
```

### 2. Cultural Heritage Preservation

Share traditional knowledge with community attribution:

1. Submit cultural stories with **CULTURAL** tier
2. Community approval required before AI training
3. Benefit sharing with cultural communities (25% + fund)
4. Anti-appropriation protections

### 3. Mental Health Research

Contribute anonymized therapeutic content:

1. Submit mental health journeys with **THERAPEUTIC** tier
2. Medical ethics oversight
3. Research fund contribution (25% + fund)
4. Professional validation required

### 4. AI Training Dataset Creation

Export training-ready datasets for AI labs:

```bash
# Export all training-ready submissions
python v45_beta/exports/export_pipeline.py \
  --format alpaca \
  --min-quality 0.7 \
  --output datasets/ysense_training_data.jsonl
```

### 5. Academic Research

Study ethical AI data practices:

- Analyze consent patterns
- Study quality metrics
- Research attribution systems
- Investigate revenue sharing models

---

## 🗺️ Roadmap

### v4.5-Beta (Current - November 2025)

- [x] Story-first AI-native UX
- [x] Collaborative 3-word distillation
- [x] Z-Protocol v2.0 integration
- [x] GDPR-compliant privacy
- [x] Attribution engine (SHA-256 + DID)
- [x] Quality metrics (6 signals)
- [x] Export pipeline (JSONL, Alpaca, ShareGPT)

### v5.0 (Q1 2026)

- [ ] Blockchain integration (Ethereum/Polygon)
- [ ] Smart contracts for revenue distribution
- [ ] IPFS/Arweave storage
- [ ] Mobile app (iOS/Android)
- [ ] Multi-language support (10+ languages)
- [ ] Community features (sharing, comments)

### v6.0 (Q2 2026)

- [ ] VerifiMind-PEAS API (attribution as a service)
- [ ] Platform partnerships (integrate with other platforms)
- [ ] AI lab marketplace (sell datasets directly)
- [ ] Advanced analytics dashboard
- [ ] Automated quality validation
- [ ] Cultural community governance

### Long-Term Vision

- **Industry Standard**: Z-Protocol adopted by 100+ platforms
- **Ecosystem**: 10,000+ users contributing ethical AI training data
- **Revenue**: $1M+ distributed to content creators
- **Impact**: Change how AI models are trained globally

---

## 🤝 Contributing

We welcome contributions from developers, researchers, and community members!

### Ways to Contribute

- **Code**: Fix bugs, add features, improve performance
- **Documentation**: Write guides, tutorials, translations
- **Research**: Study ethical AI practices, publish findings
- **Community**: Help users, answer questions, organize events
- **Feedback**: Report bugs, suggest features, share use cases

### Getting Started

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Check [open issues](https://github.com/YOUR_USERNAME/YSense-AI-Attribution-Infrastructure/issues)
3. Join our [Discord](https://discord.gg/ysenseai) (coming soon)
4. Fork the repository and submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/YSense-AI-Attribution-Infrastructure.git
cd YSense-AI-Attribution-Infrastructure

# Create feature branch
git checkout -b feature/your-feature-name

# Install dev dependencies
pip install -r requirements_dev.txt

# Run tests
pytest tests/

# Submit pull request
git push origin feature/your-feature-name
```

---

## 📝 Citation

If you use YSenseAI in your research, please cite:

```bibtex
@software{ysenseai_v45_beta,
  author = {Alton (creator35lwb)},
  title = {YSenseAI: Ethical AI Training Data Platform},
  version = {4.5-beta},
  year = {2025},
  month = {11},
  url = {https://github.com/YOUR_USERNAME/YSense-AI-Attribution-Infrastructure},
  doi = {10.5281/zenodo.17737995}
}

@misc{zprotocol_v2,
  author = {Alton (creator35lwb)},
  title = {Z-Protocol v2.0: Ethical Framework for AI Attribution and Cultural Protection},
  year = {2025},
  month = {11},
  url = {https://doi.org/10.5281/zenodo.17072168},
  doi = {10.5281/zenodo.17072168}
}
```

See [CITATION.cff](CITATION.cff) for machine-readable citation metadata.

---

## 📄 License

### Code License

YSenseAI platform code is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Alton (creator35lwb)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Full license text in LICENSE file]
```

### Z-Protocol License

Z-Protocol v2.0 framework is licensed under **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.

This means:
- ✅ You can use Z-Protocol in your projects
- ✅ You can modify and adapt it
- ✅ You must give appropriate credit
- ✅ You must share adaptations under the same license

See [LICENSE-ZPROTOCOL](LICENSE-ZPROTOCOL) for details.

### Third-Party Licenses

- Streamlit: Apache 2.0
- Anthropic Claude: Commercial API (requires key)
- Alibaba Cloud Qwen: Commercial API (requires key)

See [THIRD_PARTY_LICENSES.md](docs/THIRD_PARTY_LICENSES.md) for complete list.

---

## 🙏 Acknowledgments

### Core Team

- **Founder**: Alton (creator35lwb)
- **Z-Protocol Design**: Community-driven ethical framework
- **Platform Development**: Open-source contributors

### AI Partners

- **Anthropic**: Claude API for AI analysis and distillation
- **Alibaba Cloud**: Qwen API for quality metrics

### Community

- Beta testers who provided invaluable feedback
- Open-source contributors who improved the platform
- Cultural communities who shaped the Z-Protocol

### Inspiration

- **Creative Commons**: For showing how open licensing can change the world
- **GDPR**: For setting the standard for user privacy rights
- **Indigenous Data Sovereignty**: For teaching us about cultural protection

---

## 📞 Contact

- **Website**: https://ysenseai.org (v4.1 prototype live)
- **Email**: alton@ysenseai.org or creator35lwb@gmail.com
- **Privacy**: alton@ysenseai.org or creator35lwb@gmail.com
- **Legal**: alton@ysenseai.org or creator35lwb@gmail.com
- **GitHub**: https://github.com/YOUR_USERNAME/YSense-AI-Attribution-Infrastructure
- **Discord**: Not yet available (planned for v5.0)
- **Twitter**: https://x.com/creator35lwb

---

## ⭐ Star History

If you find YSenseAI useful, please star the repository to show your support!

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/YSense-AI-Attribution-Infrastructure&type=Date)](https://star-history.com/#YOUR_USERNAME/YSense-AI-Attribution-Infrastructure&Date)

---

**Built with ❤️ for ethical AI development**

© 2025 Alton (creator35lwb) | [MIT License](LICENSE) | [Z-Protocol v2.0](https://doi.org/10.5281/zenodo.17072168)
