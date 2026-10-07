# YSenseAI Deep Analysis and Market Sentiment Report

**Prepared for:** Alton (creator35lwb), founder of YSenseAI
**Date:** 7 October 2026
**Scope:** `YSense-AI-Attribution-Infrastructure` (branch `ccr-e4d27557-3lj801`, head `a54a0f6`), `YSense-Platform-v4.1-Fresh` (empty), the public Hugging Face footprint, the sister project VerifiMind-PEAS, and the AI training-data market as of October 2026.

---

## 1. Executive summary

YSenseAI is a thesis-first project. The thesis is strong and timely: consented, attributed, culturally specific human-written data will be worth more as the open web fills with synthetic text and as courts and regulators push AI labs toward licensed sources. The market research in Part B confirms that direction almost everywhere we looked.

The implementation, however, has not kept pace with the thesis. The repository is roughly 8,400 lines of Python spread over seven near-duplicate Streamlit apps, with no test suite, no CI, no running production instance we could reach, and several defects that stop the documented entry point from starting at all. The public Hugging Face demo does not call any AI model. The last commit to this repository was 1 March 2026; your energy since then has visibly moved to VerifiMind-PEAS, which is in much better engineering shape.

The gap between the narrative (white paper, Z-Protocol, defensive publications, AI Council) and the shipped product is the single biggest risk to the project. It is also the most fixable one, because the thesis and the documents are real assets.

**Headline verdict:** keep the thesis, retire most of the current code, and ship one small, honest, verifiable thing in the next 90 days: a 500-to-1,000-item consented, attributed, Malaysian and Southeast Asian wisdom dataset on Hugging Face, with a Croissant metadata card and per-record consent fields, produced by a thin pipeline you can actually run. That artifact is what the market is paying attention to, and it is the thing nobody else in your niche has yet.

---

## Part A: Project deep analysis

### 2. What the project actually contains

| Area | Files | Lines | State |
|---|---|---|---|
| Streamlit app variants (`v45_beta/app_*.py`) | 7 | ~4,060 | Seven forks of the same app; only `app_final.py` and `app_production.py` import correctly |
| Attribution + quality (`v45_beta/attribution/`) | 2 | 753 | Runs; self-tests pass |
| Database (`v45_beta/database/schema.py`) | 1 | 485 | Runs; SQLite, unsalted SHA-256 passwords |
| Consent (`v45_beta/consent/`) | 3 | 1,014 | Dead code carried from v4.1; imports SQLAlchemy and a `.database` module that do not exist |
| AI integrations (`v45_beta/agents/`) | 2 | 369 | Thin wrappers; pinned to a Claude 3 Haiku model past its retirement date |
| Export pipeline | 1 | 422 | Works standalone; not wired into any app |
| Root `attribution_engine.py` (defensive publication) | 1 | 470 | Separate, older design; not used by the app |
| `backend/` FastAPI + perception toolkit | 2 | 38 | Placeholder stubs ("created during git operations") |
| `prototype/` Node server | 1 | 395 | Sept 2025 pilot; in-memory |
| Documentation (md, pdf, yaml) | ~50 | n/a | Extensive: white paper v1.1, Z-Protocol v2.0/2.1, Genesis Master Prompt v16.1, legal pack, API spec |

Tests: one `test_integration.py` script and `if __name__ == "__main__"` self-tests. No pytest suite, no `.github/` workflows, no linting, no type checking.

The second repository, `YSense-Platform-v4.1-Fresh`, is empty on GitHub (no commits, no default branch). It should be archived or deleted to avoid confusing visitors.

### 3. What works

- **Attribution engine** produces deterministic SHA-256 content fingerprints, a stable `did:ysense:<hash>` author identifier, and verifies tamper-evidence correctly. The self-test passes on Python 3.13.
- **Database layer** initialises, registers users, creates sessions, and stores submissions with JSON-encoded layers. The self-test passes.
- **Export pipeline** emits JSONL, Alpaca, ShareGPT, CSV metadata, and a dataset card. Sample outputs are committed in `v45_beta/test_exports/`.
- **Legal pack** (privacy policy, beta terms, consent flow) is unusually complete for a solo project and already names GDPR, Malaysia PDPA, and Singapore PDPA.
- **Z-Protocol v2.1** is a genuine intellectual contribution: the honest reframing of "withdrawal" as "exclusion from future training, not erasure from trained weights" is more candid than most commercial data vendors' terms. It is a differentiator worth protecting.
- **Publication hygiene** is good: Zenodo DOIs, `CITATION.cff`, `.zenodo.json`, CC BY-SA on the framework, MIT on code.

### 4. Defects found (verified)

Each item below was reproduced in this session, not inferred.

1. **The documented entry point cannot start.** The README tells users to run `v45_beta/app_legal_protected.py`. That file imports `Database`, `AnthropicAgent`, `QwenAgent`, `LAYER_PROMPTS`, and `Z_PROTOCOL_TIERS`. None of those names exist. The real names are `YSenseDatabase`, `AnthropicClient`, `QWENClient`, `PERCEPTION_LAYERS`, and `CONSENT_TIERS`. The app raises `ImportError` on launch. The Dockerfile runs a different file, `app_final.py`, which does import correctly.
2. **`app_v45_beta.py` imports `YSenseOrchestrator`** from both agent modules. No such class exists. Same failure mode.
3. **Consent manager is dead code.** `consent/consent_manager.py` imports `sqlalchemy` and a relative `.database` module. Neither is in the repository or in `requirements_production.txt`. `consent_dashboard_revenue.py` imports `pandas`, also undeclared. The eight-consent-type audit trail described in the README is therefore not actually recorded by any runnable app.
4. **A real Alibaba Qwen API key is still in git history.** The redaction commits of 8 February 2026 removed it from the working tree, but the key is present in eight historical blobs across four files. Anyone who clones the public repo can recover it with one `git log -p` command. It must be rotated at Alibaba Cloud today, regardless of whether you also rewrite history.
5. **Passwords are unsalted SHA-256.** `schema.py` hashes passwords with `hashlib.sha256(password)`. This is not acceptable for a platform that asks for personal and "therapeutic" tier stories. Use `bcrypt`, `argon2-cffi`, or at minimum `hashlib.scrypt` with a per-user salt.
6. **"Cryptographic signature" is a hash, not a signature.** `_generate_signature` is `sha256(content_hash + did + app_id)`. There is no private key, so nothing can be verified against a public key and the record does not prove authorship. The `did:ysense:` method is likewise a bare hash prefix and is not resolvable under any W3C DID method. These are fine as placeholders but the README, white paper, and demo call them "cryptographic signing" and "DID", which a technical reviewer at an AI lab or a university will test in minutes.
7. **The pinned model is retired.** `config.py` defaults to `claude-3-haiku-20240307`, whose scheduled retirement date (19 April 2026) has passed. On a fresh deployment the AI calls will fail and silently fall through to the hard-coded fallback strings, which still mention a "€15K Q1 2026 target" and "humanoid robotics". Switch to a current model such as `claude-haiku-4-5` for cost or `claude-sonnet-5-5` for quality, and remove the marketing text from the fallback path.
8. **The quality gate rejects the project's own canonical example.** Running the shipped rendang story through `QualityMetricsCalculator` then `AttributionEngine._is_training_ready` returns `False` (context efficiency 0.56 and emotional richness 0.41 fall below the 0.60/0.65 thresholds). Quadrupling the story length pushes cultural specificity and emotional richness *down* because both metrics count a fixed English keyword list against total words. A Bahasa Melayu story scores similarly to the English one because the metric does not understand it. In short, the six metrics are keyword heuristics that do not measure what their names claim, and almost no real submission will ever be flagged "training ready".
9. **The Hugging Face demo does not use AI.** `YSenseAI/wisdom-canvas/app.py` returns canned strings for all five layers ("Physical presence and embodied experience are woven throughout the narrative."), picks the first three words longer than five letters as the "essence", and computes "quality" from word counts. Its README says it is "Powered by VerifiMind PEAS v0.5.0" and shows "AI Analysis". The Space has 0 likes. A visitor who pastes two different stories and gets identical layer text will conclude the project is vapourware. Either wire a real model (a Haiku 4.5 call costs well under a cent per story) or relabel the Space as a UX mock-up.
10. **Five-layer schema drift.** `layer_config.py` and the attribution engine use narrative/somatic/attention/synesthetic/temporal. `qwen_integration_v45.py` asks the model for surface/emotional/contextual/wisdom/cultural. The export format, the white paper, and the backend README each describe a slightly different set. Pick one and freeze it.
11. **Tier systems contradict each other.** The code (`layer_config.py`, `attribution_engine.py`) knows tiers 1/3/4 at 15/25/30 percent. The legal pack uses Public/Personal/Cultural/Sacred/Therapeutic at 15/20/25/30/25 percent. Z-Protocol v2.1 and the white paper use Tier 1 to 5 (0/15/20/25/30 percent) where Tier 5 is "no AI training" yet carries the highest revenue share. A contributor reading all three will not know what they agreed to. This is a consent-validity problem, not just a documentation one.
12. **Revenue estimate is fabricated in the UI.** `app_final.py` line 240 shows "Est. Revenue" as `submissions × €15`. No licensing revenue exists yet (the terms of service say so). Showing a euro figure invites a misrepresentation claim under Malaysian consumer law and GDPR transparency rules. Show "€0 (no licensing deals yet)" or remove the tile.
13. **Database path and multi-process safety.** `schema.py` holds one SQLite connection with `check_same_thread=False` in a Streamlit process, and the Dockerfile `chmod 777`s the directory. Cloud Run containers are ephemeral, so the production database is lost on every redeploy. Any real pilot needs Postgres, Turso, or at minimum a mounted volume with backups.

### 5. Architecture and engineering assessment

- **Seven app forks** are the main source of drift. The Streamlit files share 80 to 90 percent of their code; each fix was applied to one. Delete six and keep `app_final.py` (or better, extract `pipeline.py` with no UI dependency and make the app a 200-line shell on top).
- **No API surface.** The OpenAPI spec in `api/specifications/` and the FastAPI stub in `backend/` are the parts an AI lab or a research partner would actually integrate with, and they are empty. For a licensing business the API and the dataset are the product; the Streamlit UI is a contributor-acquisition tool.
- **Documentation outweighs code by a wide margin.** This is not inherently bad for a methodology project, but the README's "Production ready", "GDPR compliant", "supports thousands of concurrent users" (white paper) and "205 automated tests" (that number belongs to VerifiMind-PEAS, not this repo) will be read as claims about this codebase. Over-claiming is the fastest way to lose a technical reviewer.
- **Dependency pins are stale.** `streamlit==1.29.0` and `anthropic==0.39.0` are a year or more behind; the current Anthropic Python SDK is 1.x with a different HTTP backend. Expect install failures on Python 3.13.
- **Observability and ops.** No structured logging, no health endpoint beyond Streamlit's built-in, no error tracking, no backups. VerifiMind-PEAS has all of these; port that scaffolding here.

### 6. Positioning and narrative assessment

- **Strengths:** a clear "why" (consent, attribution, compensation, cultural protection); a defensible, published framework (Z-Protocol v2.1, two DOIs); a Malaysian and Southeast Asian cultural angle that global vendors lack; the honesty move on data withdrawal; a founder who has demonstrated sustained output across a dozen repositories.
- **Weaknesses:** market sizing in the white paper ("$100 billion attribution crisis", "€5 billion TAM", "25,000 universities at €50-200K each") is asserted rather than sourced, and the revenue plan (€15K in Q1 2026, €195K in 2026, €500K in 2027) has already missed its first milestone. Reviewers and grant committees will check these.
- **Signal dilution:** the GitHub account has 23 repositories (MarketPulse, SawitSense, GodelAI, RoleNoteAI, LegacyEvolve, AgentOS, NaturalApp, NXS-Go, MACP, three VerifiMind repos). Combined stars across all of them are under ten. Every new project divides the already small audience. The AI Council, FLYWHEEL TEAM, MACP, Genesis Prompt framing is interesting to you and to a small circle of multi-agent enthusiasts, but it is noise to a contributor who wants to share a story or a lab that wants to license data.
- **Traction signals (public):** 1 star, 0 forks, 0 issues, 0 PRs from outsiders on this repo; HF Space 0 likes; two small HF datasets with 12 and 15 downloads (both for other projects); VerifiMind-PEAS 2 stars, 1 fork, listed in the MCP Registry, v0.5.64 released 24 September 2026. There is no public evidence of registered contributors, submitted stories, or a licensing conversation.

---

## Part B: Market sentiment and development heading (October 2026)

### 7. Legal and licensing landscape: the wind is at your back, but it blows toward provenance, not "ethics"

**Courts have converged on a rule that is good for YSenseAI.** In the United States, training on lawfully acquired material is being treated as fair use (Bartz v. Anthropic, June 2025; Kadrey v. Meta, June 2025), but *how* the data was acquired is where liability lives. Anthropic's US$1.5 billion settlement, given final approval on 20 July 2026, priced pirated books at roughly US$3,000 per work across about 482,000 works. Strike 3 v. Meta (June 2026) held that the torrent download itself is the infringement. The Third Circuit's Thomson Reuters v. Ross decision (29 September 2026) is the first appellate ruling and found that training a competing product on a rival's content is not fair use. In Europe, Munich's GEMA v. OpenAI (November 2025) held a developer directly liable for lyrics memorised in model weights. The New York Times v. OpenAI fair-use cross-motions were filed 4 September 2026 and are still pending.

What this means: labs now pay to de-risk acquisition. A verifiable chain of lawful, consented acquisition is a purchasable asset. That is the exact thing your attribution record is supposed to be, which is why the "signature" and "DID" need to become real (see defect 6).

**Public price benchmarks exist now.** Two numbers are widely cited: about US$3,000 per book from the Anthropic settlement, and US$5,000 per title for three years in the HarperCollins and Microsoft deal (split 50/50 with authors, opt-in). Publisher deals run from US$20 to 25 million per year (Amazon and the New York Times) up to US$250 million over five years (News Corp and OpenAI). Reddit reported US$43 million of data-licensing revenue in Q2 2026 and is moving its renewals to usage-based pricing. Microsoft's Publisher Content Marketplace (launched 3 February 2026) pays per use when content grounds an answer. None of these benchmarks are per-token; they are per-work or per-use. Your 15 to 30 percent revenue-share framing should be re-expressed in those units.

**Where the money moved.** Scraped pretraining text has a marginal price near zero plus a liability tail. Consented expert output is where spend went: Mercor reports a US$2 billion annualised run rate (July 2026), Handshake AI about US$1.1 billion, Surge AI over US$1.2 billion, Prolific about US$350 million. Hourly rates for contributors range from US$8 to 20 per hour for general tasks to US$40 to 400 per hour for domain experts. Labs are buying evaluations, rubrics, agentic trajectories, and expert-written reasoning, not prose. This is the most important sentiment shift for YSenseAI: the "5-layer chain of thought" framing is closer to what buyers want than "stories" is, if the layers are written by humans and are verifiably human.

**Regulation is fragmenting, which favours a jurisdiction-tagged licence model.**
- EU AI Act general-purpose AI obligations have applied since 2 August 2025; enforcement powers started 2 August 2026, and the AI Office sent its first requests for information to OpenAI, Anthropic, Google and others on 29 August 2026. The public training-content summaries that labs published are widely criticised as thin ("publicly available datasets, more than 10 trillion tokens"). The European Parliament's March 2026 report calls for a machine-readable opt-out standard and an EUIPO register. A platform that emits per-source, machine-readable summaries can be sold as compliance tooling.
- The United Kingdom abandoned the text-and-data-mining opt-out approach in March 2026 with no replacement legislation.
- The US Copyright Office's Part 3 report (May 2025) was never finalised; the Department of Justice sided with OpenAI in September 2026.
- Japan adopted a non-binding disclosure "Principles Code" on 25 August 2026. Singapore's AI and IP consultation runs until 22 October 2026. Malaysia's June 2026 AI governance bill, the first in ASEAN, proposes treating training inputs and outputs as intellectual property. If enacted, YSenseAI's home jurisdiction becomes one of the more protective ones, which is a story you can tell to local funders.
- On privacy, the European Data Protection Board's Opinion 28/2024 says unlawfully processed data can taint the model and regulators may order deletion of the model itself; erasure is the board's 2026 coordinated enforcement priority. Z-Protocol v2.1's honesty about unlearning is therefore aligned with the regulators' own view, and it is ahead of most vendors.

**Consent and attribution plumbing is being standardised, but nobody honours it yet.** Cloudflare now blocks AI training crawlers by default and relaunched Pay Per Crawl as "Pay Per Use" on 15 September 2026; AI training's share of crawl requests rose from 22 percent (spring 2025) to 52 percent (June 2026). Really Simple Licensing (RSL) has a v1.0 spec and a collective with more than 50 publishers including Reddit, Yahoo, Medium, and Quora, but no public payment flows. The IETF AI Preferences drafts are still not working-group consensus and no major crawler honours them. Creative Commons Signals is in alpha. C2PA Content Credentials are widely deployed for provenance (OpenAI signs every image, TikTok has labelled over 1.3 billion videos) but say nothing about consent. Fairly Trained has about 20 small certified developers and no frontier lab.

Implication: emitting RSL licence terms, an IETF Content-Usage declaration, CC Signals vocabulary, and C2PA manifests from your export pipeline is cheap and makes YSenseAI interoperable with every emerging standard before any of them has winners. That is a better use of engineering time than a blockchain integration.

### 8. Demand side: what buyers want, and where YSenseAI's data fits

**The data wall is a pretraining problem and it is further away than the 2024 headlines said.** Epoch AI's current estimate is roughly 300 trillion tokens of quality-adjusted public human text, with median exhaustion around 2028 (range 2026 to 2032). The Stanford AI Index 2026 repeats the warning and adds that there is still no definitive evidence synthetic data can fully replace real data in pretraining. Labs are responding with curation (deduplication, filtering, pruning), not with retail story collection. Do not pitch YSenseAI as a solution to the data wall; buyers will not believe a few thousand stories move that needle.

**Three adjacent demand pockets are real and under-served, and YSenseAI touches all three:**

1. **Verified human-authored provenance as a premium.** Roughly 74 percent of new 2025 web pages contain AI-generated text; practitioners now advise keeping 20 to 30 percent of supervised fine-tuning mixes verifiably human; ISBNdb is selling pre-2022 print books to labs specifically as "slop-free" data. The human slice of post-training mixes is small but load-bearing. Your attribution chain, if it becomes real, is a provenance certificate.
2. **Evaluation data and human judgment.** Humanity's Last Exam paid US$5,000 per accepted question; LMArena raised US$150 million at a US$1.7 billion valuation on a human-preference dataset. Hallucination rates on the AI Index's new benchmark run from 22 to 94 percent, and labs need culturally grounded evaluations they cannot synthesise. A few hundred expert-validated Malaysian cultural questions or judgment pairs would be more valuable per item than thousands of stories.
3. **Cultural, multilingual, and emotional-range data.** Malay is under 5 percent of Southeast Asian model training data; SEA-LION settled on 55 percent Southeast Asian language tokens; MyCulture (about 2,600 expert-validated Malay questions) is the first Malaysian culture benchmark. Companion models (Character.AI about 20 million monthly users) show a documented narrow emotional range, with boundary-keeping emotions nearly absent; Anthropic's US$5 million wellbeing grants fund open evaluations of exactly this. The somatic and temporal layers in your toolkit are an unusually direct match for that gap.

**Hugging Face is the distribution layer, and the niche is empty.** The Hub crossed 1 million datasets in August 2026, but usage is extremely concentrated: about 86 percent of repositories have fewer than 200 lifetime downloads. Small human-curated datasets do break through when they are well documented or included in a major mixture: LIMA (1,000 rows) has about 123,000 downloads, No Robots (10,000 rows, explicitly not model-generated) about 259,000, Aya (human-written, 65 languages) about 187,000, OpenAssistant about 523,000. The mechanism is inclusion in an open post-training mix (Tulu-3 ingests No Robots, OASST1, and Aya). Hub searches for "personal stories", "cultural wisdom", or "human-written persona" return nothing. Croissant metadata with responsible-AI fields is now mandatory for the NeurIPS 2026 datasets track and the Hub generates it automatically; gated datasets with an access form are the standard consent mechanism. A realistic first-year outcome for a well-documented niche human dataset from an unknown author is hundreds to low thousands of downloads; the 100,000-plus tier needs a paper, a known organisation, or mixture inclusion.

**Platform and tooling trends.**
- Streamlit remains healthy as a Snowflake-owned internal-tool framework but the 2026 consensus is that it is unfit for consumer-facing products (websocket server per user, slow on mobile, poor auth and routing). Cloud Run users report US$1 to 2 per day even idle. Keep Streamlit for a curator console; do not build the public contributor funnel on it. Gradio on Hugging Face Spaces is the right surface for demos; Next.js plus FastAPI or Reflex for a real contributor app.
- The Model Context Protocol (MCP) was donated to the Linux Foundation's Agentic AI Foundation in December 2025, with more than 97 million monthly SDK downloads and over 12,000 public servers by April 2026. An MCP server is now the default distribution surface for a data tool, and you already know how to ship one (VerifiMind-PEAS is in the MCP Registry).
- Multi-agent "council" workflows for solo builders are mainstream (Perplexity Model Council, Manus, Claude Code). They are a production method, not a product differentiator; buyers care about the dataset, not the team that produced it.
- Defensive publication via Zenodo DOI is a recognised prior-art strategy and enters examiner search files. It blocks others' patents; it creates no enforceable rights and no revenue.

**Funding reality for ethics-first data commons.** The pattern is clear: they survive as grant-funded nonprofits or academic consortia (Mozilla Common Voice with 750,000 contributors; EleutherAI's Common Pile; Common Corpus), rarely as venture companies. Venture-backed consent marketplaces show the buyer side is institutional, not retail (Vana has about 1.3 million users but roughly US$200,000 of value locked and an unproven demand side). Programmes open now and matched to your profile:

| Programme | Fit | Amount | Note |
|---|---|---|---|
| NLnet NGI Zero Commons Fund | Strongest | EUR 5,000 to 50,000 | Bi-monthly calls; 124 awards in the last two rounds; built for solo ethical-infra projects |
| Anthropic Claude for Open Source | Easy | 6 months of Max 20x | Free tooling for a public open-source project |
| Anthropic wellbeing evaluation grants | Good | up to US$5 million pool | Open evals of emotional range in AI; direct fit for the somatic layer |
| Cradle Elevate (Malaysia) | Good | RM10 million programme | April 2026 early-stage accelerator |
| MDAG-AI (MDEC) | Conditional | up to 70 percent reimbursed, cap RM2 million | Requires Malaysia Digital status company |
| Khazanah Dana Impak | Later stage | RM2.6 billion deployed | Publicly "seeking more startups" (August 2026) |
| AI Singapore SEA-LION | Partner, not funder | n/a | Natural home for a Malay and Southeast Asian slice |

Mozilla MOSS is on indefinite hiatus; Ford and Sloan's digital infrastructure fund is research-only; Google.org and Microsoft AI for Good are skills and nonprofit programmes with poor fit.

### 9. Public and developer sentiment on "get paid for your data"

- **The public is pro-consent and anti-scrape.** YouGov: 44 percent say models should not train on internet data versus 20 percent who say they should; only 22 percent believe companies usually ask permission. Pew (25 countries, 2025): a median 34 percent are more concerned than excited about AI. Ipsos AI Monitor 2025: only 48 percent trust companies using AI to keep their data safe.
- **"Human-made" carries measurable trust value.** Reuters Institute: comfort with fully AI-made news is 12 percent versus 62 percent for human-made; weekly chatbot news use reached 10 percent in 2026 but trust in chatbot answers is 20 percent.
- **Cash dividends read as pennies.** Vana payouts are "a few dollars" for most users and its chief executive has conceded that individual data is not very valuable on its own. Generalist AI-training gig work pays US$15 to 50 per hour; expert reviewers earn US$85 to 450 per hour. Attribution, control, and revocability resonate with the public more than small cash payments do. Nobody has published a 2025 to 2026 survey measuring willingness to contribute personal data for pay; a 200-respondent survey of Malaysian contributors would be a citable, fundable research output on its own.
- **Developer sentiment toward "ethical AI" branding is sceptical.** Developers respond to artefacts they can download, evaluate, and cite; they discount manifestos, councils, and certifications. The projects in this space that developers respect (No Robots, Common Pile, Aya) led with the dataset and the paper, then the ethics.

**Net sentiment reading for YSenseAI's heading:** positive on the thesis, neutral-to-negative on the current execution, and strongly positive on a pivot toward a small, verifiable, culturally specific, human-authored evaluation and post-training dataset with machine-readable consent. The market will reward the artefact, not the framework.

### 10. Competitive landscape: the category got funded and consolidated while YSenseAI stood still

Between mid-2025 and mid-2026 the "consent-first AI data" idea went from fringe to venture-backed and Big-Tech-consolidated.

**Infrastructure giants absorbed the marketplaces.** Cloudflare acquired Human Native in January 2026 and folded it into Pay Per Crawl, now "Pay Per Use", which answers more than a billion HTTP 402 responses per day. Microsoft launched its Publisher Content Marketplace in February 2026. Protege acquired Calliope Networks and raised about US$65 million in total (a16z led the January 2026 round), claiming 20x growth in 2025. These companies now own the lab relationships and the compliance paperwork.

**Pay-the-individual models exist at scale and win on volume, not ethics.** Kled has over 200,000 users uploading 1.5 to 3 million items per day and was the number one finance app on the App Store (US$6.5 million at a US$150 million valuation; popular in the Philippines at US$20 to 40 per user per month). Luel (Y Combinator W26) raised a US$31.2 million seed, has 500,000 contributors in 96 countries, and reached US$2 million annual recurring revenue six weeks after demo day. Wirestock has 700,000 creators, a US$23 million Series A, and a run rate above US$40 million. Troveo has paid more than US$20 million to content owners. Datacurve has paid more than US$1 million in engineering bounties.

**Crypto "data dignity" plays have users but no economics.** Vana has 300-plus DataDAOs and 1.3 million testnet users, and early Reddit DataDAO contributors earned US$300 to 400, but the token is down about 97 percent from its high and Reddit banned its subreddit. Story Protocol (US$2.25 billion valuation) delayed its token unlock in February 2026 with on-chain revenue near zero and is pivoting to off-chain human-data licensing. Ocean Protocol narrowed its scope after leaving the ASI Alliance. The lesson for your v5.0 roadmap (Ethereum/Polygon, smart contracts, IPFS/Arweave): on-chain attribution without buyers produces no revenue and the market has already run that experiment.

**Provenance standards matured fast.** C2PA Content Credentials is the de facto standard (6,000-plus Content Authenticity Initiative members; Google Pixel 10 ships camera-level credentials). Adobe's "Do Not Train" preference is honoured so far only by Firefly and Spawning. Croissant is a NeurIPS submission requirement and is embedded in Hugging Face, Kaggle, and OpenML. Training-data attribution research (influence functions, FAR.AI's Concept Influence, February 2026) is productised by Bria and ProRata as "pay by influence on output". Next to these, SHA-256 plus a home-grown DID looks home-grown.

**Nobody does what YSenseAI does.** The marketplaces trade images, video, voice, code, expert question-answer pairs, and publisher text. Journaling apps (Rosebud with 500 million words journaled and a US$6 million seed, Mindsera with 80,000 users, Day One, Journey, Reflectly, Stoic) explicitly promise *not* to train on or sell entries. Personal-clone products (Delphi, Personal.ai) monetise a person's knowledge through paid chat access, and creators keep at least 85 percent. Indigenous and cultural data sovereignty work (CARE principles, Local Contexts TK and BC labels, Te Hiku's Kaitiakitanga licence) is governance and labelling, not a compensated marketplace. First-person narrative and cultural wisdom as a distinct data class with graduated consent is unoccupied space. The open question is whether there is buyer demand for it, and the demand-side evidence (Section 8) says the demand is there only if the data is framed as evaluation and post-training material with verified provenance.

**Southeast Asia is the one place where YSenseAI has home advantage.** AI Singapore's SEA-LION (S$70 million national programme), SEACrowd (498 datasheets), ILMU (YTL AI Labs; ILMUchat launched June 2026), and MaLLaM (Mesolitica) all need Bahasa Melayu and Southeast Asian cultural text. AI Malaysia Berhad was launched in July 2026 to run the National AI Action Plan 2026 to 2030, which includes data stewardship as an enabler, and the National AI Office's chief executive has said publicly that Bahasa Melayu is severely under-represented in global corpora. None of the funded marketplaces above are chasing this.

**Comparison table (abridged; full data in the research annex).**

| Name | Category | Contributor share | Traction or funding (2026) | Relevance |
|---|---|---|---|---|
| Human Native (Cloudflare) | Licensing marketplace | n/a (B2B) | Acquired Jan 2026; 1B+ 402s/day | Distribution channel, not a competitor to build against |
| Protege | Governed data marketplace | n/a (B2B) | ~US$65M raised; 20x growth | The buyer-side counterparty you would sell through |
| Created by Humans | Author AI rights | Authors keep 85%+ | US$5M seed; 100+ bestselling authors | Closest "individual sets rights" analogue; books only |
| Wirestock | Creator multimodal data | 65 to 85% to creator | 700K creators; US$40M+ run rate | Benchmark for take rate |
| Luel | Rights-cleared multimodal | n/a | US$31.2M seed; 500K contributors | Out-executes on ops |
| Kled | Pay users for uploads | Paid per task | 200K users; #1 finance app | Mass-market, no consent tiers |
| Datacurve | Expert coding data | Bounties | US$17.7M; US$1M+ paid | Shows labs pay for expert-produced data |
| ProRata.ai | Attribution at inference | 50/50 with publisher | US$75M+; 700+ publications | Model for per-use "wisdom citations" |
| Vana | Data DAOs, crypto | 80% of fees to DAO | 1.3M testnet users; token down 97% | Cautionary tale for the blockchain roadmap |
| Story Protocol | IP on chain | Token | US$2.25B valuation; on-chain revenue ~0 | Same lesson |
| Spawning | Opt-out registry, public-domain sets | Free | Honoured by Stability, HF, Adobe | Natural partner for opt-out propagation |
| Local Contexts, Te Hiku | Indigenous data governance | Non-commercial | Paid Hub memberships; licence copied with caution | Direct model for Cultural and Sacred tiers |
| SEA-LION, SEACrowd, ILMU, MaLLaM | Regional LLMs and data hubs | Grant or corporate | Active, state-backed | Natural first buyers and partners |
| Rosebud, Mindsera, Day One | AI journaling | Subscription; no training | Rosebud US$6M; 500M words | Opposite data stance; possible opt-in export partners |

**Revenue-share optics are inverted.** Every creator-facing platform found pays the creator the majority (Wirestock 65 to 85 percent, Delphi and Created by Humans 85 percent or more, ProRata 50 percent, Vana 80 percent to the DAO). YSenseAI's "15 to 30 percent to the contributor" is the platform's cut in everyone else's terms. Unless this is renamed or inverted, it will read as the least generous offer in the market, which is fatal for a project whose entire pitch is fairness.

---

## Part C: Feedback, valuation of what you have, and recommendations

### 11. Honest scorecard

| Dimension | Score (1 to 5) | Reasoning |
|---|---|---|
| Thesis and timing | 5 | Courts, regulators, and the slop-filled web all push toward consented, provenance-bearing, human-authored data. The thesis has aged well. |
| Framework and IP | 4 | Z-Protocol v2.1's honesty on unlearning is ahead of the market; two DOIs; clear licensing. Loses a point for three contradictory tier schemes. |
| Niche selection | 4 | First-person cultural wisdom with graduated consent is unoccupied, and Southeast Asia is a documented, state-acknowledged data gap where you live. |
| Shipped software | 1.5 | Documented entry point does not start; demo uses no AI; no tests, no CI, dead consent module, retired model pin, leaked key in history. |
| Data asset | 1 | No public dataset exists. One founder wisdom drop and three example JSON files. This is the thing buyers and partners would evaluate. |
| Traction | 1 | 1 star, 0 forks, 0 issues, 0 external PRs, 0 Space likes, no evidence of contributors or buyers. |
| Economics | 1.5 | Revenue share is inverted relative to every peer; revenue milestones already missed; no pricing in buyer units. |
| Narrative discipline | 2 | Over-claims ("production ready", "thousands of concurrent users", "cryptographic signing") and 23 repositories dilute a small audience. |
| Founder capability | 4 | Sustained output, real shipping ability demonstrated on VerifiMind-PEAS (v0.5.64, MCP Registry, tests, Cloud Run). The skills exist; they have not been applied here since March. |

**What the project is worth today, in practical terms:** as a company or product, close to nothing, because there is no dataset, no users, and no buyer conversation. As a *position*, it is worth a lot more than that: a published framework, a registered DOI trail, a credible founder story, an unoccupied niche, and a home region whose government is actively looking for Bahasa Melayu data stewardship projects. That position has a shelf life. Luel and Kled are adding hundreds of thousands of contributors a quarter; if one of them adds a "cultural stories" category with a consent toggle, the differentiation is gone.

### 12. Feedback on the current heading (v5.0 and v6.0 roadmap)

The README's v5.0 plan is blockchain (Ethereum/Polygon), smart contracts for revenue distribution, IPFS/Arweave storage, a mobile app, ten languages, and community features. v6.0 adds an attribution API, an AI-lab marketplace, and analytics. Against the October 2026 evidence:

- **Blockchain and smart contracts:** stop. Story Protocol and Vana ran this experiment with hundreds of millions of dollars and produced near-zero revenue and collapsed tokens. Buyers want a signed manifest and an audit log, not a chain. Spend the effort on real signatures (Ed25519 keys per contributor) and C2PA manifests instead.
- **Mobile app and community features:** premature. There is no web product that works yet, and you have no contributors to form a community.
- **Ten languages:** right instinct, wrong order. Do two well: English and Bahasa Melayu (plus Manglish as it is actually written). That is the slice the regional labs need and nobody else has.
- **Attribution-as-a-service API (v6.0):** this should be v5.0, and it should be an MCP server plus a small REST surface, because that is how labs and agent builders now discover data tools.
- **AI-lab marketplace:** do not build one. List on Protege, Troveo, Human Native/Cloudflare, or Microsoft's marketplace with Z-Protocol terms embedded in the licence. Distribution is their business; the data is yours.

### 13. Recommendations

#### 13.1 This week (security and credibility, under one day of work)

1. **Rotate the Alibaba Qwen key** that is recoverable from git history. Then either rewrite history with `git filter-repo` and force-push, or accept that the old key is public and rely on rotation. Rotation is mandatory either way.
2. **Fix or delete `app_legal_protected.py`** so the README's run command works, or change the README to point at `app_final.py`. Delete the other five app variants.
3. **Replace the retired model pin** with a current one and remove the marketing copy from the API fallback path. For cost, `claude-haiku-4-5`; for quality on layer extraction, `claude-sonnet-5-5`. Update the Anthropic SDK pin to the current 1.x line.
4. **Relabel the Hugging Face Space** as a UX mock-up, or wire a real model call behind a rate limit. Replace "Powered by VerifiMind PEAS" and "AI Analysis" until that is true.
5. **Remove the "Est. Revenue €N" tile** and any text claiming production readiness, thousands of concurrent users, or 205 tests, from this repository's README and white paper references.
6. **Archive `YSense-Platform-v4.1-Fresh`** (empty) and consider archiving or consolidating the ten-plus side repositories that are not VerifiMind or YSenseAI, so a visitor to your profile sees two focused projects.

#### 13.2 Next 30 days (make the claims true)

7. **Unify the tier model.** Pick one scheme, express it in one table, and use it in code, legal text, white paper, and dataset card. Suggested: five tiers named Public, Personal, Cultural, Sacred, Therapeutic, each with (a) who may train, (b) withdrawal meaning per v2.1, (c) share of licensing revenue. Drop the "Tier 5 no training at 30 percent" construction; a tier that earns nothing cannot carry a share.
8. **Invert the revenue-share language.** State it as "contributors receive 70 to 85 percent of net licensing revenue; YSenseAI retains 15 to 30 percent for operations and the community fund." This is what the code's existing percentages can mean if you read them as the platform's cut, and it is the only framing that survives comparison with Wirestock, Delphi, and Created by Humans.
9. **Make the signature real.** Generate an Ed25519 keypair per contributor at registration (store the private key encrypted with the user's password-derived key, or let them hold it), sign the content hash, and publish the public key in the attribution record. Adopt `did:key` rather than an invented `did:ysense` method so any DID resolver can verify it. Emit a C2PA manifest alongside, with a custom assertion carrying consent tier, DID, and licence terms. Salt and stretch passwords with argon2 while you are in that file.
10. **Rebuild the quality metrics as model-graded rubrics, not keyword counts.** Have a model score each of the six dimensions 1 to 5 against a written rubric, store the rubric version, and sample 10 percent for human review. Report inter-rater agreement in the dataset card. This turns a fake metric into a defensible one and is itself a publishable method.
11. **Add the engineering scaffolding you already have in VerifiMind-PEAS:** pytest with at least the three self-tests converted, a GitHub Actions workflow (lint, tests, `pip-audit`), structured logging, and a Postgres or Turso backend so Cloud Run redeploys do not erase the database.
12. **Freeze one five-layer schema** (narrative, somatic, attention, synesthetic, temporal) across prompts, exports, docs, and the white paper.

#### 13.3 Next 90 days (ship the artefact the market rewards)

13. **Publish YSenseAI Wisdom v0.1 on Hugging Face as a gated dataset: 500 to 1,000 consented, attributed stories with the five layers, distillation, consent tier, signed attribution, and a Croissant card with responsible-AI fields.** Seed it yourself and with 20 to 50 Malaysian contributors you recruit personally (family, community, university students, oral-history groups). Target at least 40 percent Bahasa Melayu or Manglish. This single artefact does more for credibility, partnerships, and grants than every document in the repository combined, and the Hub search for this niche is currently empty.
14. **Derive an evaluation set from it.** 200 to 300 items that test cultural grounding and emotional range (for example, "what would a Malaysian elder say here" with human-validated answers, or paired responses rated for boundary-keeping emotion). Evaluation data commands per-item prices that stories never will, and it is what Anthropic's wellbeing grants and the regional labs are buying.
15. **Ship an MCP server** that exposes dataset search, attribution verification, and consent-tier lookup. You have already done this for VerifiMind-PEAS; reuse the scaffolding. List it in the MCP Registry.
16. **Make the export pipeline emit the standards:** Croissant, Data Provenance card, RSL licence terms, an IETF Content-Usage declaration, CC Signals vocabulary, and a per-source EU AI Act Article 53 summary fragment. Each is a few dozen lines, and together they make YSenseAI interoperable with every emerging standard before any has won.
17. **Open three partner conversations with the artefact in hand:** AI Singapore's SEA-LION team, YTL AI Labs (ILMU) or Mesolitica (MaLLaM), and AI Malaysia Berhad under the 2026 to 2030 action plan's data-stewardship enabler. Ask for inclusion in a training or evaluation mixture, not for money. Inclusion is how No Robots and Aya became influential.
18. **Apply for NLnet NGI Zero Commons (EUR 5,000 to 50,000) in the next bi-monthly round, Anthropic's Claude for Open Source, and Cradle Elevate.** The NLnet application should be about the consent-and-attribution schema plus the dataset, not about the AI Council.
19. **Run a 200-respondent contributor survey** (Malaysia first) on willingness to contribute reflective and cultural text under each consent tier and at each compensation framing. No such survey exists for 2025 to 2026; it is citable, fundable, and tells you whether your tiers match what people want.
20. **Launch sequence once v0.1 is live:** Show HN with the dataset and the honest withdrawal framing as the hook, then the Hugging Face community post, then a short arXiv or Zenodo note describing the consent schema and the rubric-based quality method. Lead every post with the artefact and the honesty, not the council.

#### 13.4 Positioning sentence to replace the current one

Current: "Build your personal wisdom library while contributing to ethical AI development."

Suggested: "Verified human-written, consented stories and cultural knowledge from Southeast Asia, with machine-readable provenance and consent, for post-training and evaluation. Contributors keep the majority of licensing revenue and can see exactly which models trained on their words."

### 14. What to stop doing

- Stop adding repositories and frameworks (AgentOS, GodelAI, LegacyEvolve, NaturalApp, MACP) until YSenseAI and VerifiMind each have a shipped artefact with external users. Every new repository halves the attention the existing ones get.
- Stop describing production readiness, GDPR compliance, user capacity, or test counts that this repository does not have.
- Stop treating the AI Council as a public differentiator. It is a good production method; keep it internal and lead with outputs.
- Stop planning blockchain, smart contracts, mobile, and ten languages for v5.0. The market has priced those at zero.

### 15. Metrics that would show the heading is working (by January 2027)

| Metric | Now | Target |
|---|---|---|
| Public dataset items (consented, signed, Croissant) | 0 | 500 to 1,000 |
| Bahasa Melayu or Manglish share | 0 | 40 percent |
| Dataset downloads (Hugging Face) | 0 | 500 to 2,000 |
| External contributors with signed consent | 0 | 50 |
| Regional lab or institute evaluating the set | 0 | 2 |
| Grant applications submitted | 0 | 3 (NLnet, Cradle, Anthropic OSS) |
| CI passing, tests, zero leaked secrets | No | Yes |
| GitHub stars (this repo) | 1 | 50 to 100 (a Show HN that lands can do this in a day) |

---

## Annex: method and sources

**Code analysis** was performed on the local checkout at commit `a54a0f6` (1 March 2026): every Python file was compiled, the attribution, quality, and database self-tests were run on Python 3.13, import graphs were traced for all seven app variants, git history was scanned for secrets, and the quality gate was tested against the project's own sample story, a lengthened version, and a Bahasa Melayu version. The Hugging Face Space source was read directly from the Hub.

**Market research** was conducted on 7 October 2026 by three parallel research passes (legal and licensing; competitors and adjacent initiatives; demand side, ecosystem, and funding) using live web search and page fetches, roughly 160 tool calls in total. Figures from analyst estimates, single-source reports, or company-reported numbers are flagged as such in the text. Some primary sites (ysenseai.org, verifimind.io, zenodo.org, huggingface.co web, epoch.ai, pewresearch.org) were unreachable through this session's network policy, so those facts come from secondary coverage or from the Hugging Face API connector.

Selected sources: Authors Guild on the Anthropic settlement (authorsguild.org); Ballard Spahr and Copyright Lately on Thomson Reuters v. Ross; Latham & Watkins on Getty v. Stability; Norton Rose Fulbright on GEMA v. OpenAI and Kadrey v. Meta; Mayer Brown and Praxikon on EU AI Act GPAI enforcement; Lewis Silkin on the UK copyright decision; Japan Times on Japan's disclosure code; Baker McKenzie on Singapore's consultation; Pebblous on Malaysia's AI governance bill; EDPB Opinion 28/2024; The Register and Digiday on RSL; IETF AIPREF drafts; Content Authenticity Initiative 2026 state report; TechCrunch on Mercor, Luel, Rosebud, and Cloudflare policy; Sacra on Handshake, Surge, Prolific, Datacurve; SiliconANGLE on Protege and LMArena; Techinformed on Cloudflare and Human Native; CoinDesk on Story Protocol; The Block on Vana; Business Wire on Troveo and ProRata; Pulse2 on Wirestock; Stanford AI Index 2026 coverage (Forbes, IEEE Spectrum); Epoch AI data-wall estimates via PBS and Silicon Canals; Hugging Face State of Open Models Summer 2026 via TechJack; NeurIPS 2026 dataset track requirements; YouGov, Pew, Ipsos, and Reuters Institute surveys; NLnet funding pages; TechNode and The Star on Cradle and Khazanah; The Edge and ai.gov.my on AI Malaysia; SEA-LION, SEACrowd, MyCulture, and ILMU papers and pages; Local Contexts and Te Hiku Media on Indigenous data governance.
