# Consilience 🧠🔭

**See any topic through multiple disciplinary lenses simultaneously — scientific, philosophical, economic, cultural, historical, and ethical.**

Type any question or topic, select 2 or more perspectives, and get a structured multi-lens analysis: a confidence-weighted view from each discipline, areas where the perspectives agree, points of conflict, and a final synthesis that bridges them all.

---

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
- ✅ **Next.js 15 App Router** — fast SSR + client interactivity
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
pnpm lint     # ESLint check
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
| **Framework** | Next.js 15 (App Router) |
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

**Made with ❤️ by [SUDARSHANCHAUDHARI](https://github.com/SUDARSHANCHAUDHARI)**

[⭐ Star this repo](https://github.com/SUDARSHANCHAUDHARI/Consilience) · [🐛 Report Issue](https://github.com/SUDARSHANCHAUDHARI/Consilience/issues)

</div>
