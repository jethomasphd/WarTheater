#!/usr/bin/env node
/**
 * Paper 2 — build the publication-ready Word manuscript.
 *
 *   NODE_PATH=<dir with node_modules> node make_docx.js
 *
 * Reads the pipeline outputs (output/tables/*.csv, output/figures/*.png) and
 * writes paper2_healthcare_collapse.docx next to this script. Requires the
 * `docx` npm package; everything else is Node stdlib. The narrative text
 * mirrors manuscript/paper2_healthcare_collapse.md (the canonical source).
 */
const fs = require("fs");
const path = require("path");
const {
  AlignmentType, BorderStyle, Document, Footer, HeadingLevel, ImageRun,
  LevelFormat, PageNumber, Packer, Paragraph, ShadingType, Table, TableCell,
  TableRow, TextRun, WidthType,
} = require("docx");

const HERE = __dirname;
const FIG = (n) => path.join(HERE, "..", "output", "figures", n);
const TAB = (n) => path.join(HERE, "..", "output", "tables", n);

// ---------------------------------------------------------------- helpers --
const FONT = "Georgia";
const num = (x, d = 2) => Number(x).toFixed(d);

function readCsv(p) {
  const [head, ...rows] = fs.readFileSync(p, "utf8").trim().split("\n");
  const cols = head.split(",");
  return rows.map((r) => {
    // minimal CSV parse (our tables quote only description-free fields)
    const vals = [];
    let cur = "", inQ = false;
    for (const ch of r) {
      if (ch === '"') inQ = !inQ;
      else if (ch === "," && !inQ) { vals.push(cur); cur = ""; }
      else cur += ch;
    }
    vals.push(cur);
    return Object.fromEntries(cols.map((c, i) => [c, vals[i]]));
  });
}

// Parse **bold** / *italic* markers into TextRuns. Backticks (inline code in
// the md source) render as plain text in the Word manuscript.
function runs(text, base = {}) {
  text = text.replace(/`/g, "");
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const tok = m[0];
    if (tok.startsWith("**")) out.push(new TextRun({ text: tok.slice(2, -2), bold: true, ...base }));
    else out.push(new TextRun({ text: tok.slice(1, -1), italics: true, ...base }));
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}

const P = (text, opts = {}) => new Paragraph({
  children: runs(text), spacing: { after: 160, line: 276 },
  alignment: AlignmentType.JUSTIFIED, ...opts,
});
const H1 = (text) => new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 320, after: 160 } });
const H2 = (text) => new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 120 } });

function figure(file, caption) {
  const data = fs.readFileSync(FIG(file));
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 200, after: 60 },
      children: [new ImageRun({ data, type: "png", transformation: fit(file) })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 240 },
      children: runs(caption, { size: 18, color: "444444" }),
    }),
  ];
}

// scale each figure to 6.5in width (626px/in at our 200dpi savings ~ use px ratio)
const sizePng = (buf) => ({ w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) });
function fit(file) {
  const { w, h } = sizePng(fs.readFileSync(FIG(file)));
  const W = 624;                        // ~6.5" at 96dpi
  return { width: W, height: Math.round((h / w) * W) };
}

function table(headers, rows, colw) {
  const total = colw.reduce((a, b) => a + b, 0);
  const cell = (t, opts = {}) => new TableCell({
    width: { size: opts.w, type: WidthType.DXA },
    shading: opts.head ? { type: ShadingType.CLEAR, fill: "EDF2F7" } : undefined,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({
      alignment: opts.left ? AlignmentType.LEFT : AlignmentType.RIGHT,
      children: runs(String(t), { size: 17, bold: !!opts.head }),
    })],
  });
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: colw,
    rows: [
      new TableRow({ tableHeader: true, children: headers.map((t, i) => cell(t, { head: true, w: colw[i], left: i === 0 })) }),
      ...rows.map((r) => new TableRow({ children: r.map((t, i) => cell(t, { w: colw[i], left: i === 0 })) })),
    ],
  });
}
const tcap = (text) => new Paragraph({
  spacing: { before: 200, after: 100 }, children: runs(text, { size: 18 }),
});
const spacer = () => new Paragraph({ spacing: { after: 160 }, children: [] });

// ---------------------------------------------------------------- content --
const phase = readCsv(TAB("t01_phase_summary.csv"));
const proj = readCsv(TAB("t06_projection.csv"));
const dive = readCsv(TAB("t07_divergence.csv"));
const medi = readCsv(TAB("t04_mediation.csv"));
const slop = readCsv(TAB("t05_simple_slopes.csv"));
const anov = readCsv(TAB("t02_anova.csv"));
const leth = readCsv(TAB("t02_lethality.csv"));
const sens = readCsv(TAB("t07_confidence_sensitivity.csv"));

const t1rows = phase.map((r) => [
  r.phase, r.days, num(r.strikes_mean), num(r.civfac_strikes_mean),
  `${num(r.iran_civ_mean)} (${r.iran_civ_total})`, r.iran_mil_total,
  `${num(r.leb_mean)} (${r.leb_total})`, r.killed_total_total,
]);

const t2rows = anov.map((r) => [
  r.outcome_label, `${num(r.anova_F, 1)}`, r.welch_F === "" || r.welch_F === undefined || r.welch_F === "nan" || Number.isNaN(Number(r.welch_F)) ? "undef.†" : num(r.welch_F, 1),
  num(r.kruskal_H, 1), num(r.eta2, 3), num(r.omega2, 3), "< .001",
]);

const t4rows = medi.map((r) => [
  r.sample === "full" ? "Full war (n=170)" : "Major Combat (n=40)",
  r.outcome === "iran_civ" ? "Iranian civilian" : "All-faction",
  num(r.a_X_to_M, 3), num(r.b_M_to_Y, 3), num(r.c_total, 3), num(r.c_prime_direct, 3),
  `${num(r.indirect_ab, 3)} [${num(r.boot_ci_lo, 3)}, ${num(r.boot_ci_hi, 3)}]`,
  num(Number(r.prop_mediated) * 100, 1) + "%",
]);

const slopRows = slop
  .filter((r) => r.sample === "full" && r.at_W !== "JN_boundary")
  .map((r) => [
    r.moderator === "hssi_pct" ? "HSSI (21 audited events)" : "Facility damage (benchmarks)",
    r.at_W, num(r.slope, 3), num(r.se, 3),
    Number(r.p) < 0.001 ? "< .001" : num(r.p, 3),
  ]);

const projRows = ["floor_1to1", "low_3to1", "avg_4to1", "high_15to1"].map((sc) => {
  const ir = proj.find((r) => r.population === "Iran" && r.scenario === sc);
  const lb = proj.find((r) => r.population === "Lebanon" && r.scenario === sc);
  const lab = { floor_1to1: "1:1 (floor)", low_3to1: "3:1 (low)", avg_4to1: "4:1 (average)", high_15to1: "15:1 (upper)" }[sc];
  const f = (x) => Number(x).toLocaleString("en-US");
  return [lab,
    `${f(ir.indirect_lower)}–${f(ir.indirect_upper)}`, `${f(ir.total_lower)}–${f(ir.total_upper)}`,
    `${f(lb.indirect_lower)}–${f(lb.indirect_upper)}`, `${f(lb.total_lower)}–${f(lb.total_upper)}`];
});

const diveRows = dive.map((r) => {
  const f = (x) => Number(x).toLocaleString("en-US");
  return [`Day ${r.day}`, r.scope, `${f(r.min_value)} (${r.min_source})`,
          `${f(r.max_value)} (${r.max_source})`, num(r.divergence_ratio, 2) + "×"];
});

const sensRows = ["strikes_milfac", "strikes_civfac", "retal"].map((term) => {
  const g = (v) => sens.find((r) => r.variant === v && r.term === term);
  const lab = { strikes_milfac: "Military-facing locations", strikes_civfac: "Civilian-facing locations", retal: "Retaliation tempo" }[term];
  const fmt = (r) => `${num(r.coef, 2)} (${num(r.se_hac, 2)})${r.sig || ""}`;
  return [lab, fmt(g("all")), fmt(g("high_only")), fmt(g("weighted"))];
});

// Body text blocks (kept in sync with the .md manuscript, the canonical text).
const md = fs.readFileSync(path.join(HERE, "paper2_healthcare_collapse.md"), "utf8");
function section(startMarker, endMarker) {
  const i = md.indexOf(startMarker);
  const j = endMarker ? md.indexOf(endMarker) : md.length;
  if (i < 0 || j < 0) throw new Error(`marker not found: ${startMarker} / ${endMarker}`);
  return md.slice(i + startMarker.length, j).trim();
}
// paragraphs from a md block, skipping md tables/headings/rules
function paras(block, opts = {}) {
  return block.split(/\n\n+/)
    .map((s) => s.replace(/\n/g, " ").trim())
    .filter((s) => s && !s.startsWith("|") && !s.startsWith("#") && !s.startsWith("---") && !s.startsWith("**Table"))
    .map((s) => P(s, opts));
}

// ------------------------------------------------------------------ build --
const children = [];

// Title block
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { before: 1200, after: 240 },
  children: runs("The Direct Toll Is a Floor: Civilian-Facing Targeting, Health-System Degradation, and Mortality in the First 170 Days of the 2026 US–Iran War", { size: 40, bold: true }),
}));
for (const line of [
  "Working paper — Paper 2 of the IranWar.ai research-agenda series",
  "Prepared from the IranWar.ai Event-Level Research Dataset, v1.2 (Days 1–170; 2026-02-28 to 2026-08-16)",
  "Dashboard: https://iranwar.ai   •   Repository: github.com/jethomasphd/WarTheater",
  "All results reproduce from ResearchData/Paper2/ (bash run_all.sh; seeded, ~1 minute)",
]) {
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: runs(line, { size: 20, color: "444444" }),
  }));
}

// Abstract
children.push(H1("Abstract"));
for (const part of ["**Background.**", "**Methods.**", "**Results.**", "**Conclusions.**"]) {
  const startIdx = md.indexOf(part);
  const nxt = { "**Background.**": "**Methods.**", "**Methods.**": "**Results.**", "**Results.**": "**Conclusions.**", "**Conclusions.**": "**Keywords:**" }[part];
  const txt = md.slice(startIdx, md.indexOf(nxt)).replace(/\n/g, " ").trim();
  children.push(P(txt));
}
children.push(P(md.slice(md.indexOf("**Keywords:**"), md.indexOf("## 1. Introduction")).replace(/\n/g, " ").replace(/---/g, "").trim()));

// 1 Introduction
children.push(H1("1. Introduction"));
children.push(...paras(section("## 1. Introduction", "## 2. Data")));

// 2 Data
children.push(H1("2. Data"));
children.push(H2("2.1 Source and pinning"));
children.push(...paras(section("### 2.1 Source and pinning", "### 2.2 Outcomes")));
children.push(H2("2.2 Outcomes"));
children.push(...paras(section("### 2.2 Outcomes", "### 2.3 Exposures")));
children.push(H2("2.3 Exposures"));
children.push(...paras(section("### 2.3 Exposures", "### 2.4 The health-system")));
children.push(H2("2.4 The health-system insult register and two degradation curves"));
children.push(...paras(section("insult register and two degradation curves", "## 3. Statistical methods")));

// 3 Methods
children.push(H1("3. Statistical methods"));
children.push(...paras(section("## 3. Statistical methods", "## 4. Results")));

// 4 Results
children.push(H1("4. Results"));
children.push(H2("4.1 The shape of mortality"));
children.push(...paras(section("### 4.1 The shape of mortality (Table 1; Figures 1–3)", "**Table 1.")));
children.push(tcap("**Table 1.** Per-phase summary (daily means; totals in parentheses)."));
children.push(table(
  ["Phase", "Days", "Strikes/d", "Civ-facing/d", "Iran civ/d (tot)", "Iran mil (tot)", "Lebanon/d (tot)", "All killed"],
  t1rows, [1500, 900, 950, 1150, 1500, 1150, 1450, 1000]));
children.push(spacer());
children.push(...figure("fig1_mortality_trajectory.png",
  "**Figure 1.** Kinetic exposure and daily estimated deaths across the four phases. Iranian mortality is confined almost entirely to Major Combat; the Lebanon front carries the ceasefire period."));
children.push(...figure("fig2_cumulative_burden.png",
  "**Figure 2.** Cumulative burden: the daily-series and snapshot accountings (their divergence is analyzed in §4.7), children killed, and displacement."));
children.push(...figure("fig3_health_system_timeline.png",
  "**Figure 3.** Health-system degradation: the 21 audited insult events (HSSI) and the benchmark-anchored facility-damage curve (31 → 307 → 309 facilities)."));

children.push(H2("4.2 Phase comparisons"));
children.push(...paras(section("### 4.2 Phase comparisons (Table 2; Figure 4)", "### 4.3")));
children.push(tcap("**Table 2.** One-way phase comparisons (df1 = 3). † Welch undefined where a phase has zero variance (Iranian civilian deaths are uniformly 0 in two phases); Kruskal–Wallis carries the robustness burden."));
children.push(table(
  ["Outcome", "ANOVA F", "Welch F", "K–W H", "η²", "ω²", "p"],
  t2rows, [2600, 1050, 1050, 1000, 900, 900, 900]));
children.push(spacer());
children.push(...figure("fig4_phase_comparison.png",
  "**Figure 4.** Daily deaths by phase (boxes: IQR and median; points: individual days, seeded jitter)."));

children.push(H2("4.3 Which component of the violence predicted death"));
children.push(...paras(section("### 4.3 Which component of the violence predicted death (Table 3)", "### 4.4")));

children.push(H2("4.4 Mediation: civilian-facing targeting carries the association"));
children.push(...paras(section("### 4.4 Mediation: civilian-facing targeting carries the association (Table 4; Figure 5)", "### 4.5")));
children.push(tcap("**Table 4.** Single-mediator results: X = military-facing tempo, M = civilian-facing tempo. Bootstrap: 10,000 seeded day-resamples, percentile CIs."));
children.push(table(
  ["Sample", "Outcome", "a", "b", "c", "c′", "a×b [95% CI]", "% mediated"],
  t4rows, [1750, 1450, 750, 750, 750, 750, 2100, 1100]));
children.push(spacer());
children.push(...figure("fig5_mediation_paths.png",
  "**Figure 5.** The mediation model with full-sample estimates."));

children.push(H2("4.5 Moderation: what a strike cost as the system degraded"));
children.push(...paras(section("### 4.5 Moderation: what a strike cost as the system degraded (Table 5; Figure 6)", "### 4.6")));
children.push(tcap("**Table 5.** Simple slopes of Iranian civilian deaths on strike tempo at degradation = mean ± 1 SD (full sample, HAC covariance)."));
children.push(table(
  ["Moderator", "At W", "Slope", "SE", "p"],
  slopRows, [3100, 900, 900, 900, 900]));
children.push(spacer());
children.push(...figure("fig6_moderation.png",
  "**Figure 6.** (A) Simple slopes under the HSSI moderator; points are observed days colored by degradation tercile. (B) The two degradation operationalizations."));

children.push(H2("4.6 The floor and the tail: projecting indirect mortality"));
children.push(...paras(section("### 4.6 The floor and the tail: projecting indirect mortality (Table 6; Figure 7)", "**Table 6.")));
children.push(tcap("**Table 6.** Projected deaths at Day 170 under literature indirect:direct ratios. Ranges span the two internal direct-toll bases (daily series / terminal snapshot). Scenario arithmetic, not estimates from these data."));
children.push(table(
  ["Ratio", "Iran — indirect", "Iran — total", "Lebanon — indirect", "Lebanon — total"],
  projRows, [1500, 1900, 1900, 1900, 1900]));
children.push(spacer());
// Everything between the md's Table 6 block and §4.7; paras() drops the
// markdown table rows, keeping the prose intact. The marker is the full
// caption line so no fragment of it survives the slice.
children.push(...paras(section(
  "**Table 6. Projected total conflict deaths at Day 170 under literature indirect:direct ratios.**",
  "### 4.7")));
children.push(...figure("fig7_indirect_projection.png",
  "**Figure 7.** Projected total conflict deaths under each ratio; whiskers span the internal direct-toll bounds."));

children.push(H2("4.7 Reading the disagreements: the flood, quantified"));
children.push(...paras(section("### 4.7 Reading the disagreements: the flood, quantified (Table 7; Figure 8)", "**Table 7.")));
children.push(tcap("**Table 7.** Divergence summary: cumulative Iranian-toll claims and dataset-internal accountings."));
children.push(table(
  ["Moment", "Scope", "Low", "High", "Ratio"],
  diveRows, [900, 2300, 2800, 2800, 800]));
children.push(spacer());
children.push(tcap("**Table 8.** The core model (Iranian civilian deaths/day) under data-confidence variants of the exposure series. Cells: coefficient (HAC SE); *** p < .001. Direction and magnitude are stable; the HIGH-only variant loses precision through discarded rows."));
children.push(table(
  ["Exposure term", "All rows", "HIGH-only", "Confidence-weighted"],
  sensRows, [2600, 1800, 1800, 2000]));
children.push(spacer());
children.push(...figure("fig8_source_divergence.png",
  "**Figure 8.** (A) Cumulative-toll claims by source family against the dataset's own two accountings, with the Day-45 spread and the Day-57 re-anchoring. (B) Core-model coefficients (95% CI) under the three confidence variants."));

// 5-7
children.push(H1("5. Discussion"));
children.push(...paras(section("## 5. Discussion", "## 6. Limitations")));
children.push(H1("6. Limitations"));
children.push(...paras(section("## 6. Limitations", "## 7. Conclusion")));
children.push(H1("7. Conclusion"));
children.push(...paras(section("## 7. Conclusion", "## Reproducibility")));

// Reproducibility
children.push(H1("Reproducibility"));
children.push(P("cd ResearchData/Paper2 && python3 -m pip install -r requirements.txt && bash run_all.sh — regenerates the panel, the audited health-system register, all tables, and all figures from the frozen v1.2 dataset release in about one minute. Bootstraps are seeded (SEED = 42); every curated constant (register audit decisions, benchmark anchors, toll claims, WASH rows) is verified against the dataset at run time by anchor-text assertion. Design decisions: docs/METHODS.md. Variable definitions: docs/CODEBOOK_panel.md. Plain-language analysis guide for the first author: docs/STUDENT_GUIDE.md."));

// References
children.push(H1("References"));
const refBlock = section("## References", "*Dataset citation:*");
for (const ref of refBlock.split(/\n- /).map((s) => s.replace(/^- /, "").replace(/\n/g, " ").trim()).filter(Boolean)) {
  children.push(new Paragraph({
    spacing: { after: 100 }, alignment: AlignmentType.LEFT,
    indent: { left: 360, hanging: 360 },
    children: runs(ref, { size: 19 }),
  }));
}
children.push(P(md.slice(md.indexOf("*Dataset citation:*")).replace(/\n/g, " ").trim()));

// ------------------------------------------------------------------- doc --
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: FONT, size: 21 } },   // 10.5pt body
      heading1: { run: { font: FONT, size: 28, bold: true, color: "1A1A1A" } },
      heading2: { run: { font: FONT, size: 24, bold: true, color: "1A1A1A" } },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },       // US Letter
        margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 },
      },
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "IranWar.ai Research Agenda — Paper 2 — page ", size: 16, color: "666666" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "666666" }),
          ],
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const out = path.join(HERE, "paper2_healthcare_collapse.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", out, `(${(buf.length / 1024).toFixed(0)} KB)`);
});
