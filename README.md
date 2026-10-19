# Consilience 🧠🔭

[![Next.js](https://img.shields.io/badge/Next.js-16-black.svg)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-backend-3776AB.svg)](https://www.python.org/)
[![Claude](https://img.shields.io/badge/Claude-Sonnet%204.6-7c3aed.svg)](https://www.anthropic.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**See any topic through multiple disciplinary lenses simultaneously — scientific, philosophical, economic, cultural, historical, and ethical.**

Type any question or topic, select 2 or more perspectives, and get a structured multi-lens analysis: a confidence-weighted view from each discipline, areas where the perspectives agree, points of conflict, and a final synthesis that bridges them all.

---

## Table of Contents

- [🌟 Features](#-features)
- [🏗️ Architecture](#-architecture)
- [🖥️ UI Overview](#-ui-overview)
- [🚀 Getting Started](#-getting-started)
- [📜 Scripts](#-scripts)
- [🔑 Environment Variables](#-environment-variables)
- [📊 Current Status](#-current-status)
- [🛠️ Tech Stack](#-tech-stack)
- [🔒 Security](#-security)
- [📄 License](#-license)
- [🤝 Contributing](#-contributing)
- [📞 Support](#-support)
- [About](#about)

## 🌟 Features

### 🔭 Core Features
- ✅ **Topic Input** — any question, concept, or debate (e.g. Universal Basic Income, Quantum Computing, Gene editing)
- ✅ **Perspective Selector** — 6 lenses: Scientific, Philosophical, Economic, Cultural, Historical, Ethical (select 2 or more)
- ✅ **Per-Perspective Cards** — each view shown with confidence bar (0–100%) and detailed position
- ✅ **Areas of Agreement** — cross-perspective common ground surfaced in green
- ✅ **Points of Conflict** — genuine disagreements surfaced in red
- ✅ **Synthesis** — AI-generated consilience statement bridging all perspectives
- ✅ **Sky-blue dark theme** — clean, readable layout

### 🤖 AI Features
- ✅ **Claude Sonnet 4.6** — generates genuinely distinct views per discipline
- ✅ **Confidence scoring** — AI rates its certainty per perspective (0–100)
- ✅ **Cross-perspective conflict detection** — identifies real tensions, not just surface differences
- ✅ **Consilience synthesis** — convergent insight beyond what any single discipline sees

### ⚙️ Technical Features
- ✅ **Next.js 16 App Router** — fast SSR + client interactivity
- ✅ **TypeScript strict mode** — fully typed analysis result interfaces
- ✅ **Tailwind CSS** — sky blue accent, animated confidence progress bars

---

## 🏗️ Architecture

```
Consilience/
├── 📁 app/
│   ├── 📄 page.tsx          # Main analysis UI
│   ├── 📄 layout.tsx        # Root layout with dark background
│   ├── 📄 globals.css       # Global styles
│   └── 📁 api/
│       └── 📁 analyze/
│           └── 📄 route.ts  # POST /api/analyze — Claude multi-perspective engine
├── 📁 public/               # Static assets
├── 📄 .env.example          # Environment variable template
├── 📄 package.json
└── 📄 README.md
```

---

## 🖥️ UI Overview

| Section | Description |
|---|---|
| **Topic Input** | Text field — any topic, question, or debate |
| **Perspective Toggles** | 6 pill buttons — select any 2 or more |
| **Analyze Button** | Triggers Claude multi-perspective analysis |
| **Perspective Cards** | Per-lens card with confidence bar + detailed view |
| **Agreement Panel** | Green panel — cross-perspective common ground |
| **Conflict Panel** | Red panel — genuine points of disagreement |
| **Synthesis Block** | Sky-blue panel — AI-generated consilience statement |

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- pnpm
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SUDARSHANCHAUDHARI/Consilience.git
   cd Consilience
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env.local
   # Edit .env.local and add your ANTHROPIC_API_KEY
   ```

4. **Run dev server**
   ```bash
   pnpm dev
   ```
   Open [http://localhost:3000](http://localhost:3000)

---

## 📜 Scripts

```bash
pnpm dev      # Start development server (Turbopack)
pnpm build    # Production build
pnpm start    # Start production server
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | ✅ Yes |

Get your key at [console.anthropic.com](https://console.anthropic.com). Add it to `.env.local` — this file is gitignored and never committed.

---

## 📊 Current Status

| Property | Value |
|---|---|
| **Version** | 1.0.0 |
| **Status** | ✅ MVP Complete |
| **Model** | claude-sonnet-4-6 |
| **Perspectives** | 6 (Scientific, Philosophical, Economic, Cultural, Historical, Ethical) |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Framework** | Next.js 16 (App Router) |
| **Language** | TypeScript (strict mode) |
| **Styling** | Tailwind CSS |
| **AI** | Claude API — claude-sonnet-4-6 |
| **Package Manager** | pnpm |

---

## 🔒 Security

- `ANTHROPIC_API_KEY` lives in `.env.local` — gitignored, never committed
- `.env.example` contains placeholder values only
- API key sent directly to Anthropic — no intermediate server
- No topic data stored or logged

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Commit your changes (`git commit -m 'feat: add your feature'`)
4. Push to the branch (`git push origin feat/your-feature`)
5. Open a Pull Request

---

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/SUDARSHANCHAUDHARI/Consilience/issues)

---

<div align="center">

**Built by Sudarshan Chaudhari — SudarshanTechLabs.** [@SUDARSHANCHAUDHARI](https://github.com/SUDARSHANCHAUDHARI)

[⭐ Star this repo](https://github.com/SUDARSHANCHAUDHARI/Consilience) · [🐛 Report Issue](https://github.com/SUDARSHANCHAUDHARI/Consilience/issues)

</div>

---

## About

I'm Sudarshan Chaudhari, a Senior Quality Engineer, Test Automation specialist, and AI systems builder based in Bangkok, Thailand.

I have 13+ years of experience in software quality engineering, working across SaaS, fintech, gaming, web, mobile, cloud, and digital signage platforms. My background combines hands-on test automation with QA leadership, test strategy, CI/CD, release quality, production investigation, and cross-platform validation.

Alongside my professional QA career, I run [SudarshanTechLabs](https://sudarshantechlabs.com/), my independent engineering and product lab where I design, build, test, and ship software across Android, web, AI, cybersecurity, developer tooling, and cross-platform applications.

### What I work on

- ⚙️ **Quality Engineering & Test Automation** — Playwright, Selenium, Cypress, Appium, API testing, automation frameworks, end-to-end testing, CI/CD, release gates, GitHub Actions, risk-based testing, and production validation
- 🤖 **AI Systems & Automation** — AI agents, multi-agent orchestration, MCP servers, AI-assisted QA, prompt tooling, developer workflows, automation systems, and Claude Code plugins
- 📱 **Mobile & Cross-Platform Applications** — Android applications built with Kotlin and Jetpack Compose, Google Play releases, automated build and publishing pipelines, and cross-platform development spanning iOS, web, Windows, and macOS
- 🌐 **Web Applications & Platforms** — Full-stack applications using Next.js, TypeScript, Firebase, Cloudflare, REST APIs, and modern web infrastructure
- 🛠️ **Developer Tooling & CLI Engineering** — Rust, Python, TypeScript, CLI utilities, multi-repository tooling, build automation, release tooling, and engineering productivity systems
- 🛡️ **Cybersecurity & Observability** — Threat detection, log analysis, security auditing, vulnerability assessment, monitoring, and security-focused developer tools
- 📺 **Digital Signage & Device Platforms** — Content validation, playback testing, device compatibility, production investigation, monitoring, and QA across diverse hardware and operating-system environments

My work sits at the intersection of quality engineering, automation, AI, and software development. I approach products with a QA mindset from the beginning: understanding failure modes, designing for testability, automating repetitive work, and building release confidence into the engineering process.

Through SudarshanTechLabs, I also build products and tools from idea to production, covering architecture, development, testing, CI/CD, release automation, monitoring, and ongoing maintenance.

🌐 [sudarshantechlabs.com](https://sudarshantechlabs.com/) · 💼 [LinkedIn](https://linkedin.com/in/sudarshan-chaudhari) · 🐙 [GitHub](https://github.com/SUDARSHANCHAUDHARI) · ✉️ [sunny.sudarshan@gmail.com](mailto:sunny.sudarshan@gmail.com)
