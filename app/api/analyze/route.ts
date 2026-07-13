import Anthropic from "@anthropic-ai/sdk";
import { guard, safeError, extractText, safeJson } from "../../../lib/apiGuard";
import { NextRequest, NextResponse } from "next/server";
const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
export async function POST(req: NextRequest) {
  const _guard = guard(req);
  if (_guard) return _guard;
  const { topic, perspectives, depth } = await req.json();
  if (!topic?.trim()) return NextResponse.json({ error: "Topic required" }, { status: 400 });
  const prompt = `You are a multi-perspective analysis expert. Analyze this topic from multiple angles to reach consilience — the convergence of evidence across disciplines.
Topic: ${topic}
Perspectives to consider: ${perspectives || "Technical, Business, User, Ethical, Market"}
Depth: ${depth || "Standard"}
Return JSON: { "topicSummary": "string", "perspectives": [{ "name": "string", "stance": "string", "keyPoints": ["string"], "confidence": 0-100, "evidence": ["string"] }], "agreements": ["string"], "conflicts": ["string"], "blindSpots": ["string"], "consilience": "string", "actionableInsights": ["string"], "verdict": "string", "uncertainties": ["string"], "summary": "string" }
Return ONLY valid JSON.`;
  try {
    const msg = await client.messages.create({ model: "claude-sonnet-4-6", max_tokens: 1500, messages: [{ role: "user", content: prompt }] });
    return NextResponse.json(safeJson(extractText(msg)));
  } catch (e) { return safeError(e); }
}
