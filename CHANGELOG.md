# Changelog

All notable changes to YSenseAI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-10-07

Week-one fixes following the October 2026 project audit. Nothing here adds a feature; it makes the documented behaviour true.

### Fixed
- The README's entry point (`app_legal_protected.py`) imported five names that did not exist and could not start. `app_final.py` is now the single canonical app and the README, Docker, and Quick Start instructions all point at it.
- `config.py` raised on import whenever either API key was missing, which stopped the app even though only Claude is used. It now warns and the app runs in offline fallback mode.
- Default Anthropic model was `claude-3-haiku-20240307`, retired 19 April 2026. Default is now `claude-haiku-4-5`, configurable with `ANTHROPIC_MODEL`.
- Offline fallback text no longer returns marketing copy that looked like real analysis; it returns a clearly labelled offline notice.
- README install and Docker commands used wrong paths, a wrong class name, and the wrong port.
- Saving a wisdom submission raised `KeyError: 'layer_responses'` because the attribution engine emits the key `layers` while the database expected `layer_responses`. Found by the new smoke test; the database now accepts both.

### Security
- Passwords are now hashed with salted scrypt. Existing unsalted SHA-256 rows still verify and are upgraded on next login.
- **Action required by the maintainer:** an Alibaba Cloud Qwen API key committed in November 2025 remains recoverable from git history despite the February 2026 redaction commits. Rotate it in the Alibaba Cloud console.

### Changed
- Registration now requires ticking privacy policy, terms of service, beta acknowledgment, and age consents, each recorded in a new `consents` table with the document version. Optional research-participation consent is recorded too.
- Export page shows the user's full consent history and offers self-service account deletion (submissions, sessions, and analytics removed; consent rows anonymised as an audit trail).
- The "Est. Revenue" tile, which multiplied submissions by €15 with no licensing deal behind it, now shows €0 and says so.
- Dependency pins moved to `anthropic>=1.0,<2`, `streamlit>=1.50,<2`, `openai>=1.0`. Unused `requests` pin dropped.
- README gains a "Known Limitations (Beta)" section stating plainly that the signature is hash-based, the DID method is unregistered, the quality metrics are heuristics, the Hugging Face Space is a mock-up, and no revenue exists yet.

### Removed
- Five duplicate or broken app variants (`app_complete.py`, `app_production.py`, `app_v2_story_first.py`, `app_v2_1_collaborative.py`, `app_v45_beta.py`) and the broken `app_legal_protected.py`. All remain in git history.
- Dead consent modules (`consent_manager.py` depended on SQLAlchemy and a module that did not exist; `consent_dashboard_revenue.py` and `consent_database.py` were never wired in). Consent recording now lives in `database/schema.py`.

### Added
- `v45_beta/tests/test_smoke.py`: attribution round trip, quality metric ranges, password hashing, database and consent flow, offline-mode client, and a check that every `from X import Y` in the app resolves.
- GitHub Actions CI workflow (compile, smoke tests, and a headless Streamlit start on Python 3.11 and 3.13), shipped at `ci/github-workflow-ci.yml` because the pushing token lacked the `workflow` scope; see `ci/README.md` to activate it.

## [4.5.0-beta] - 2025-11-27

### Added

#### Core Features
- **Story-First AI-Native UX**: Users write freely, AI extracts structured wisdom layers
- **Collaborative 3-Word Distillation**: Chat with AI to refine essence through dialogue
- **5-Layer Perception Toolkit**: Automatic extraction of Narrative, Somatic, Attention, Synesthetic, Temporal layers
- **Personal Wisdom Library**: Search, view, and manage all submissions with quality scores
- **Export Pipeline**: Download data in JSON (for personal LLM), Markdown, CSV formats

#### Z-Protocol v2.0 Integration
- **5-Tier Classification System**: Public, Personal, Cultural, Sacred, Therapeutic
- **8 Consent Types**: Granular control over data usage
- **Revenue Sharing**: 15-30% compensation based on content tier
- **Cultural Protection**: Community attribution and benefit sharing for Cultural/Sacred tiers
- **Consent Management**: Full audit trail with withdrawal rights

#### Attribution & Quality
- **Cryptographic Attribution**: SHA-256 fingerprinting + DID (Decentralized Identifier) assignment
- **Quality Metrics**: 6 training optimization signals
  - Context efficiency (300-800 token sweet spot)
  - Reasoning depth (5-layer Chain of Thought)
  - Cultural specificity (>70% unique cultural markers)
  - Emotional richness (>15 descriptors per 100 words)
  - Attention density (3+ concrete details per layer)
  - Compression quality (>80% essence preserved in 3-word distillation)
- **Training-Ready Export**: JSONL, Alpaca, ShareGPT, Dataset Card formats

#### Legal & Compliance
- **GDPR-Compliant Privacy Policy**: 19 sections covering all user rights
- **Terms of Service**: Comprehensive founder protection with beta disclaimers
- **Beta Program Disclaimers**: Clear "AS IS" and "AT YOUR OWN RISK" language
- **Cookie Consent Banner**: Essential cookies only (session, security)
- **Registration Consent Flow**: 5 required consents + 2 optional consents
- **Account Deletion**: GDPR-compliant 72-hour deletion
- **Data Export**: Full data portability (JSON/MD/CSV)

#### AI Integration
- **Anthropic Claude API**: AI analysis, layer extraction, collaborative distillation
- **Alibaba Cloud Qwen API**: Quality metrics calculation, alternative analysis
- **Fallback Mode**: Graceful degradation when APIs unavailable

#### Database
- **SQLite Schema**: Production-ready with WAL mode
- **User Management**: Authentication, session management, password hashing (SHA-256)
- **Submission Storage**: Stories, layers, essence, quality scores, attribution
- **Consent Tracking**: Full audit trail with timestamps and metadata

### Changed
- **UX Philosophy**: Shifted from "clinical questionnaire" to "organic story canvas"
- **AI Role**: AI does heavy lifting (extraction), user validates and refines
- **Distillation Flow**: From "user fills form" to "AI suggests, user refines through chat"

### Security
- **Password Hashing**: SHA-256 for all passwords
- **Session Management**: Secure session tokens
- **CSRF Protection**: Security cookies
- **Data Encryption**: All data encrypted at rest and in transit (HTTPS/TLS)

### Documentation
- **Comprehensive README**: Project overview, architecture, installation, use cases
- **CITATION.cff**: Academic citation format
- **Zenodo Metadata**: DOI assignment ready
- **CONTRIBUTING.md**: Open-source contribution guidelines
- **CODE_OF_CONDUCT.md**: Community guidelines
- **Privacy Policy**: GDPR-compliant (19 sections)
- **Terms of Service**: Beta program terms (17 sections)
- **Legal Protection Summary**: Founder protection overview

### Known Issues
- **Beta Status**: Platform is experimental and under active development
- **API Fallback**: Some features use fallback mode when APIs unavailable
- **Mobile Optimization**: UI optimized for desktop, mobile improvements planned for v5.0
- **Multi-language**: Currently English only, translations planned for v5.0

### Roadmap
See [README.md](README.md#roadmap) for detailed roadmap.

**Next Release**: v5.0 (Q1 2026)
- Blockchain integration (Ethereum/Polygon)
- IPFS/Arweave storage
- Mobile app (iOS/Android)
- Multi-language support (10+ languages)

---

## [4.1.0] - 2025-11-01

### Added
- Initial platform with 7 orchestrator agents (Y-Strategy, Y-Market, Y-Ethics, Y-Legal, Y-Revenue, Y-Documentation, Y-CEO)
- Basic wisdom submission flow
- Z-Protocol v1.0 implementation
- Revenue estimation dashboard

### Changed
- Questionnaire-based submission flow (replaced in v4.5-beta)

---

## [1.0.0] - 2025-10-01

### Added
- Initial proof-of-concept
- Basic attribution engine
- Z-Protocol v0.1 draft

---

## Version History

- **v4.5.0-beta** (2025-11-27): Story-first UX, collaborative distillation, full legal protection
- **v4.1.0** (2025-11-01): 7 orchestrator agents, Z-Protocol v1.0
- **v1.0.0** (2025-10-01): Initial proof-of-concept

---

## Semantic Versioning

YSenseAI follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes, incompatible API changes
- **MINOR** (0.X.0): New features, backward-compatible
- **PATCH** (0.0.X): Bug fixes, backward-compatible

**Beta/Alpha Suffixes**:
- `-beta`: Feature-complete, testing phase
- `-alpha`: Early development, unstable
- `-rc`: Release candidate, final testing

---

## How to Upgrade

### From v4.1.0 to v4.5.0-beta

**Database Migration**:
```bash
# Backup existing database
cp ysense_production.db ysense_production.db.backup

# Run migration script
python v45_beta/database/migrate_v41_to_v45.py
```

**Environment Variables**:
```bash
# Update .env with new API keys
ANTHROPIC_API_KEY=sk-ant-api03-...
QWEN_API_KEY=sk-...
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
```

**Dependencies**:
```bash
pip install -r requirements_production.txt
```

---

## Support

For questions, bug reports, or feature requests:

- **GitHub Issues**: https://github.com/creator35lwb-web/YSense-AI-Attribution-Infrastructure/issues
- **Email**: alton@ysenseai.org or creator35lwb@gmail.com
- **Discord**: Not yet available (planned for v5.0)

---

**Maintained by**: Alton (creator35lwb)  
**License**: MIT (code), CC BY-SA 4.0 (Z-Protocol)  
**Z-Protocol DOI**: 10.5281/zenodo.17072168
