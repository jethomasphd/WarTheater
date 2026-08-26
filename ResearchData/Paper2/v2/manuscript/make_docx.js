#!/usr/bin/env node
/**
 * Paper 2 — v2 (student-findings edition): build the Word manuscript.
 *
 *   NODE_PATH=<dir with node_modules> node make_docx.js
 *
 * Reads the v2 pipeline outputs (output/tables/*.csv, output/figures/*.png) and
 * writes paper2_v2_three_findings.docx next to this script. The narrative text
 * mirrors paper2_v2_three_findings.md (the canonical source); the three tables
 * and three figures are injected from the regenerated pipeline outputs, so the
 * Word document cannot drift from the analysis. Requires the `docx` npm package.
 */
const fs = require("fs");
const path = require("path");
const {
  AlignmentType, Document, Footer, HeadingLevel, ImageRun,
  PageNumber, Packer, Paragraph, ShadingType, Table, TableCell,
  TableRow, TextRun, WidthType,
} = require("docx");

const HERE = __dirname;
const FIG = (n) => path.join(HERE, "..", "output", "figures", n);
const TAB = (n) => path.join(HERE, "..", "output", "tables", n);
const FONT = "Georgia";
const num = (x, d = 2) => Number(x).toFixed(d);
const commas = (x) => Number(x).toLocaleString("en-US");

// ---------------------------------------------------------------- helpers --
function readCsv(p) {
  const [head, ...rows] = fs.readFileSync(p, "utf8").trim().split("\n");
  const cols = head.split(",");
  return rows.map((r) => {
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

// Parse **bold** / *italic* markers into TextRuns; drop inline-code backticks.
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
const spacer = () => new Paragraph({ spacing: { after: 160 }, children: [] });
const tcap = (text) => new Paragraph({ spacing: { before: 200, after: 100 }, children: runs(text, { size: 18 }) });

const sizePng = (buf) => ({ w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) });
function fit(file) {
  const { w, h } = sizePng(fs.readFileSync(FIG(file)));
  const W = 624;
  return { width: W, height: Math.round((h / w) * W) };
}
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

// ---- markdown slicing ----------------------------------------------------- //
const md = fs.readFileSync(path.join(HERE, "paper2_v2_three_findings.md"), "utf8");
function section(startMarker, endMarker) {
  const i = md.indexOf(startMarker);
  const j = endMarker ? md.indexOf(endMarker, i + startMarker.length) : md.length;
  if (i < 0 || j < 0) throw new Error(`marker not found: ${startMarker} / ${endMarker}`);
  return md.slice(i + startMarker.length, j).trim();
}
function splitOn(text, marker) {
  const k = text.indexOf(marker);
  return k < 0 ? [text, ""] : [text.slice(0, k), text.slice(k)];
}
function paras(block, opts = {}) {
  return block.split(/\n\n+/)
    .map((s) => s.replace(/\n/g, " ").trim())
    .filter((s) => s && !s.startsWith("|") && !s.startsWith("#") && !s.startsWith("---") && !s.startsWith("**Table"))
    .map((s) => P(s, opts));
}

// ---- injected tables from regenerated outputs ----------------------------- //
const phase = readCsv(TAB("t1_phase_summary.csv"));
const slop = readCsv(TAB("t5_simple_slopes.csv"));
const proj = readCsv(TAB("t6_projection.csv"));

const t1rows = phase.map((r) => [
  r.phase, r.days, num(r.strikes_mean),
  `${num(r.iran_civ_mean)} (${commas(r.iran_civ_total)})`, `(${commas(r.iran_mil_total)})`,
  `${num(r.leb_mean)} (${commas(r.leb_total)})`, commas(r.killed_total_total),
]);

const dmgLabel = { "-1SD": "Low (−1 SD; early war)", "mean": "Mean", "+1SD": "High (+1 SD; late war)" };
const t2rows = slop
  .filter((r) => r.moderator === "facil_damage_pct" && r.sample === "full" && r.at_W !== "JN_boundary")
  .map((r) => [dmgLabel[r.at_W] || r.at_W, num(r.slope, 2),
               Number(r.p) < 0.001 ? "< .001" : num(r.p, 3) + (r.sig ? ` ${r.sig}` : " (n.s.)")]);

const projRows = ["floor_1to1", "low_3to1", "avg_4to1", "high_15to1"].map((sc) => {
  const ir = proj.find((r) => r.population === "Iran" && r.scenario === sc);
  const lb = proj.find((r) => r.population === "Lebanon" && r.scenario === sc);
  const lab = { floor_1to1: "1:1 (floor)", low_3to1: "3:1 (low)", avg_4to1: "4:1 (average)", high_15to1: "15:1 (upper)" }[sc];
  return [lab,
    `${commas(ir.indirect_lower)}–${commas(ir.indirect_upper)}`, `${commas(ir.total_lower)}–${commas(ir.total_upper)}`,
    `${commas(lb.indirect_lower)}–${commas(lb.indirect_upper)}`, `${commas(lb.total_lower)}–${commas(lb.total_upper)}`];
});

// ------------------------------------------------------------------ build --
const children = [];

// Title block
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { before: 900, after: 240 },
  children: runs("Killed Fast, Left Fragile, Counted Short: Front-Loaded Mortality, Health-System Resilience Erosion, and the Uncounted Indirect Toll in the First 170 Days of the 2026 US–Iran War", { size: 38, bold: true }),
}));
for (const line of [
  "Working paper — Paper 2 (v2, student-findings edition) of the IranWar.ai research-agenda series",
  "First author: Eugene Osei Mensah",
  "Prepared from the IranWar.ai Event-Level Research Dataset, v1.2 (Days 1–170; 2026-02-28 to 2026-08-16)",
  "All results reproduce from ResearchData/Paper2/v2/ (bash run_all.sh; seeded, ~30 seconds)",
]) {
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: runs(line, { size: 20, color: "444444" }),
  }));
}

// About this version (framed as an italic note)
children.push(H1("About this version"));
children.push(...paras(section("## About this version", "## Abstract"), { italics: false }));

// Abstract
children.push(H1("Abstract"));
for (const part of ["**Background.**", "**Methods.**", "**Results.**", "**Conclusions.**"]) {
  const nxt = { "**Background.**": "**Methods.**", "**Methods.**": "**Results.**", "**Results.**": "**Conclusions.**", "**Conclusions.**": "**Keywords:**" }[part];
  const startIdx = md.indexOf(part);
  const txt = md.slice(startIdx, md.indexOf(nxt, startIdx)).replace(/\n/g, " ").trim();
  children.push(P(txt));
}
children.push(P(md.slice(md.indexOf("**Keywords:**"), md.indexOf("## 1. Introduction")).replace(/\n/g, " ").replace(/---/g, "").trim()));

// 1 Introduction
children.push(H1("1. Introduction"));
children.push(...paras(section("## 1. Introduction", "## 2. Data and methods")));

// 2 Data and methods
children.push(H1("2. Data and methods"));
children.push(...paras(section("## 2. Data and methods", "## 3. Finding 1")));

// 3 Finding 1 — front-loading (Table 1 + Figure 1)
children.push(H1("3. Finding 1 — The war killed fast and early"));
{
  const sec = section("## 3. Finding 1 — The war killed fast and early", "## 4. Finding 5");
  const [pre, post] = splitOn(sec, "**Table 1.");
  children.push(...paras(pre));
  children.push(tcap("**Table 1.** Per-phase summary (daily means; totals in parentheses)."));
  children.push(table(
    ["Phase", "Days", "Strikes/d", "Iran civ/d (tot)", "Iran mil (tot)", "Lebanon/d (tot)", "All killed"],
    t1rows, [1550, 900, 1000, 1650, 1350, 1650, 1100]));
  children.push(spacer());
  children.push(...paras(post));
  children.push(...figure("fig1_frontloading.png",
    "**Figure 1.** (A) Daily all-faction deaths across the four phases; Major Combat (shaded) carries the bulk. (B) The temporal concentration of mortality: 79.6% of documented deaths had accrued by the end of Major Combat — 23.5% of the war."));
}

// 4 Finding 5 — resilience erosion (Table 2 + Figure 2)
children.push(H1("4. Finding 5 — The system lost its ability to absorb shocks"));
{
  const sec = section("## 4. Finding 5 — The system lost its ability to absorb shocks", "## 5. Finding 6");
  const [pre, post] = splitOn(sec, "**Table 2.");
  children.push(...paras(pre));
  children.push(tcap("**Table 2.** Simple slope of Iranian civilian deaths on strike tempo at accumulated facility damage = mean ± 1 SD (full sample, HAC covariance)."));
  children.push(table(
    ["Accumulated facility damage", "Slope (deaths / strike location)", "p"],
    t2rows, [3400, 2600, 1400]));
  children.push(spacer());
  children.push(...paras(post));
  children.push(...figure("fig2_resilience_erosion.png",
    "**Figure 2.** (A) The strike–death slope fans open as accumulated facility damage rises: flat when the system was intact, roughly one death per additional strike location once it was heavily degraded. (B) The two degradation operationalizations over the war."));
}

// 5 Finding 6 — indirect floor (Table 3 + Figure 3)
children.push(H1("5. Finding 6 — The counted dead are only a floor"));
{
  const sec = section("## 5. Finding 6 — The counted dead are only a floor", "## 6. The three findings");
  const [pre, post] = splitOn(sec, "**Table 3.");
  children.push(...paras(pre));
  children.push(tcap("**Table 3.** Projected total conflict deaths at Day 170 under literature indirect:direct ratios. Ranges span the two internal direct-toll bases (daily series / terminal snapshot). Scenario arithmetic, not estimates from these data."));
  children.push(table(
    ["Ratio (indirect:direct)", "Iran — indirect", "Iran — total", "Lebanon — indirect", "Lebanon — total"],
    projRows, [2100, 1900, 1900, 1900, 1900]));
  children.push(spacer());
  children.push(...paras(post));
  children.push(...figure("fig3_indirect_floor.png",
    "**Figure 3.** The documented direct toll (dark, dotted line) against the projected total under each ratio (gold); whiskers span the two internal direct-toll bounds. The counted dead are the floor."));
}

// 6 The three findings as one argument
children.push(H1("6. The three findings as one argument"));
children.push(...paras(section("## 6. The three findings as one argument", "## 7. Limitations")));

// 7 Limitations, 8 Conclusion
children.push(H1("7. Limitations"));
children.push(...paras(section("## 7. Limitations", "## 8. Conclusion")));
children.push(H1("8. Conclusion"));
children.push(...paras(section("## 8. Conclusion", "## Reproducibility")));

// Reproducibility
children.push(H1("Reproducibility"));
children.push(P("cd ResearchData/Paper2/v2 && python3 -m pip install -r requirements.txt && bash run_all.sh — regenerates the panel, the audited health-system register, all focused tables, and the three figures from the frozen v1.2 dataset release in about thirty seconds. src/04_synthesis.py re-derives every headline number in this manuscript and asserts each against its reported value, so the pipeline fails loudly on any drift. Bootstraps are seeded (SEED = 42). Design decisions: docs/METHODS.md. Variable definitions: docs/CODEBOOK_panel.md. Plain-language walkthrough for the first author: docs/STUDENT_GUIDE.md."));

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
      document: { run: { font: FONT, size: 21 } },
      heading1: { run: { font: FONT, size: 28, bold: true, color: "1A1A1A" } },
      heading2: { run: { font: FONT, size: 24, bold: true, color: "1A1A1A" } },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 },
      },
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "IranWar.ai Research Agenda — Paper 2 (v2, three findings) — page ", size: 16, color: "666666" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "666666" }),
          ],
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const out = path.join(HERE, "paper2_v2_three_findings.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", out, `(${(buf.length / 1024).toFixed(0)} KB)`);
});
