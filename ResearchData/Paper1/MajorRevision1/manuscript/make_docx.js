#!/usr/bin/env node
/**
 * Paper 1 — Major Revision 1: build the Word manuscript (broadly APA 7th edition).
 *
 *   cd manuscript && npm install && node make_docx.js
 *   (or: NODE_PATH=/path/with/node_modules node make_docx.js)
 *
 * Reads paper1_major_revision1.md (the canonical text) and the regenerated pipeline
 * outputs (output/tables/*.csv, output/figures/*.png), and writes
 * Paper1_MajorRevision1.docx next to this script.
 *
 * Every table in the Word document is built from the CSV outputs, not typed. As a guard,
 * each CSV-built table is compared cell by cell with the corresponding markdown table in
 * the .md; any disagreement aborts the build. Figures are embedded from output/figures/.
 * Requires the `docx` npm package (pinned in package.json).
 */
const fs = require("fs");
const path = require("path");
const {
  AlignmentType, BorderStyle, Document, Footer, Header, HeadingLevel, ImageRun,
  LevelFormat, PageBreak, PageNumber, Packer, Paragraph, Table, TableCell, TableRow,
  TextRun, WidthType, TabStopType,
} = require("docx");

const HERE = __dirname;
const MD = path.join(HERE, "paper1_major_revision1.md");
const OUT = path.join(HERE, "Paper1_MajorRevision1.docx");
const FIG = (n) => path.join(HERE, "..", "output", "figures", n);
const TAB = (n) => path.join(HERE, "..", "output", "tables", n);

const FONT = "Times New Roman";
const BODY = 24;          // 12 pt in half-points
const SMALL = 20;         // 10 pt for tables
const DOUBLE = 480;       // double spacing
const SINGLE = 240;
const RUNNING_HEAD = "RECIPROCITY WITHOUT A LAG";
const MINUS = "−";

// ------------------------------------------------------------------ utils --
function fix(x, d) {
  // round half away from zero (avoids 1.295 -> "1.29" from binary floating point)
  const v = Number(x);
  const m = Math.pow(10, d);
  const r = Math.round((Math.abs(v) + Number.EPSILON) * m) / m;
  return ((v < 0 ? MINUS : "") + r.toFixed(d));
}
const pfmt = (p) => {  // p-value formatting used throughout the manuscript
  p = Number(p);
  if (p < 0.0005) return "< 0.001";   // would round to 0.000 at three decimals
  if (p < 0.01) return fix(p, 4);      // exact to four decimals (e.g. 0.0007)
  if (p < 0.1) return fix(p, 3);
  return fix(p, 2);
};
const pstr = (p) => { const s = pfmt(p); return s.startsWith("<") ? `p ${s}` : `p = ${s}`; };
const pct = (share) => { const v = 100 * Number(share); return v < 1 ? fix(v, 1) + "%" : fix(v, 0) + "%"; };
const dash = (s) => String(s).replace(/(\d)-(\d)/g, "$1–$2");

function readCsv(p) {
  const lines = fs.readFileSync(p, "utf8").trim().split(/\r?\n/);
  const parse = (line) => {
    const vals = []; let cur = "", inQ = false;
    for (const ch of line) {
      if (ch === '"') inQ = !inQ;
      else if (ch === "," && !inQ) { vals.push(cur); cur = ""; }
      else cur += ch;
    }
    vals.push(cur); return vals;
  };
  const cols = parse(lines[0]);
  return lines.slice(1).map((l) => Object.fromEntries(cols.map((c, i) => [c, parse(l)[i]])));
}
const rowWhere = (rows, pred) => { const r = rows.find(pred); if (!r) throw new Error("row not found"); return r; };

// Inline markdown -> TextRuns (**bold**, *italic*, `code` stripped of backticks)
function runs(text, base = {}) {
  text = text.replace(/`([^`]*)`/g, "$1");
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), font: FONT, size: BODY, ...base }));
    const tok = m[0];
    if (tok.startsWith("**")) out.push(new TextRun({ text: tok.slice(2, -2), bold: true, font: FONT, size: BODY, ...base }));
    else out.push(new TextRun({ text: tok.slice(1, -1), italics: true, font: FONT, size: BODY, ...base }));
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), font: FONT, size: BODY, ...base }));
  return out;
}
const plain = (s) => s.replace(/\*\*|\*|`/g, "");

// ------------------------------------------------------------ paragraphs --
const body = (text) => new Paragraph({
  children: runs(text), spacing: { line: DOUBLE, after: 0 },
  indent: { firstLine: 720 }, alignment: AlignmentType.LEFT,
});
const noIndent = (text, base = {}) => new Paragraph({
  children: runs(text, base), spacing: { line: DOUBLE, after: 0 }, alignment: AlignmentType.LEFT,
});
const h1 = (text) => new Paragraph({
  children: [new TextRun({ text, bold: true, font: FONT, size: BODY })],
  heading: HeadingLevel.HEADING_1, alignment: AlignmentType.CENTER,
  spacing: { line: DOUBLE, before: 240, after: 0 }, keepNext: true,
});
const h2 = (text) => new Paragraph({
  children: [new TextRun({ text, bold: true, font: FONT, size: BODY })],
  heading: HeadingLevel.HEADING_2, alignment: AlignmentType.LEFT,
  spacing: { line: DOUBLE, before: 120, after: 0 }, keepNext: true,
});
const bullet = (text) => new Paragraph({
  children: runs(text), numbering: { reference: "bullets", level: 0 },
  spacing: { line: DOUBLE, after: 0 }, alignment: AlignmentType.LEFT,
});
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });
const caption = (label, title) => [
  new Paragraph({ children: [new TextRun({ text: label, bold: true, font: FONT, size: BODY })],
    spacing: { line: DOUBLE, before: 240, after: 0 }, keepNext: true }),
  new Paragraph({ children: [new TextRun({ text: title, italics: true, font: FONT, size: BODY })],
    spacing: { line: DOUBLE, after: 0 }, keepNext: true }),
];
const note = (text) => new Paragraph({
  children: [new TextRun({ text: "Note. ", italics: true, font: FONT, size: SMALL }), ...runs(text, { size: SMALL })],
  spacing: { line: SINGLE, before: 80, after: 240 }, alignment: AlignmentType.LEFT,
});

// APA table: horizontal rules only (top, below header, bottom)
function apaTable(headers, rows, colw) {
  const total = colw.reduce((a, b) => a + b, 0);
  const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  const line = { style: BorderStyle.SINGLE, size: 8, color: "000000" };
  const cell = (t, i, opts) => new TableCell({
    width: { size: colw[i], type: WidthType.DXA },
    borders: { top: opts.top ? line : none, bottom: opts.bottom ? line : none, left: none, right: none },
    margins: { top: 40, bottom: 40, left: 60, right: 60 },
    children: [new Paragraph({
      alignment: i === 0 ? AlignmentType.LEFT : AlignmentType.CENTER,
      spacing: { line: SINGLE, after: 0 },
      children: runs(String(t), { size: SMALL, bold: !!opts.head }),
    })],
  });
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: colw,
    rows: [
      new TableRow({ tableHeader: true, children: headers.map((t, i) => cell(t, i, { head: true, top: true, bottom: true })) }),
      ...rows.map((r, k) => new TableRow({ children: r.map((t, i) => cell(t, i, { bottom: k === rows.length - 1 })) })),
    ],
  });
}

// --------------------------------------------------- tables from the CSVs --
// Each builder returns [{headers, rows, colw}] (one or more tables per number).
const PHASE_SHORT = { "Major Combat": "Combat", "First Ceasefire": "Ceasefire", "Resumption": "Resumption", "Diplomatic Pause": "Pause" };

const TABLES = {
  "1": () => {
    const t = readCsv(TAB("t01_phase_intensity.csv"));
    return [{
      headers: ["Phase", "Days", "n", "Strikes/day", "Retaliation/day", "Strike:retaliation", "Diplomatic/day", "Days with any strike (%)"],
      rows: t.map((r) => [r.phase, dash(r.days), r.n_days, fix(r.strikes_per_day, 2), fix(r.retal_per_day, 2),
        fix(r.strike_retal_ratio, 2), fix(r.diplomatic_per_day, 2), fix(r.pct_days_with_strike, 1)]),
      colw: [1500, 900, 500, 1000, 1200, 1300, 1150, 1810],
    }];
  },
  "2": () => {
    const sd = readCsv(TAB("t02_same_day.csv"))[0];
    const ls = readCsv(TAB("t02_lag_selection.csv"))[0];
    const g = readCsv(TAB("t02_granger.csv"));
    const cc = readCsv(TAB("t02_ccf_combat.csv"));
    const ir = readCsv(TAB("t02_irf_summary.csv"))[0];
    const gr = (dir) => { const r = rowWhere(g, (x) => x.sample.startsWith("combat") && x.direction === dir);
      return `F${r.df} = ${fix(r.F, 2)}, ${pstr(r.p_value)}`; };
    const c = (lag) => fix(rowWhere(cc, (x) => Number(x.lag_days) === lag).ccf, 2);
    return [{
      headers: ["Quantity", "Value"],
      rows: [
        ["Same-day Pearson r (95% CI)", `${fix(sd.pearson_r, 2)} (${fix(sd.ci95_low, 2)} to ${fix(sd.ci95_high, 2)})`],
        ["Lag order selected: AIC / BIC / HQIC / FPE", `${ls.aic} / ${ls.bic} / ${ls.hqic} / ${ls.fpe}`],
        ["Granger, strikes → retaliation (VAR(1))", gr("strikes -> retal")],
        ["Granger, retaliation → strikes (VAR(1))", gr("retal -> strikes")],
        ["Cross-correlation at lags −1 / 0 / +1 / +2", `${c(-1)} / ${c(0)} / ${c(1)} / ${c(2)}`],
        ["Impulse response of retaliation to a strike shock, day 0 (95% band)",
          `${fix(ir.impact_response_h0, 2)} (${fix(ir.impact_ci95_low, 2)} to ${fix(ir.impact_ci95_high, 2)}) events`],
        ["Cumulative response over 7 days", `${fix(ir.cumulative_7day, 2)} events`],
        ["First day on which the band includes zero", `Day ${ir.first_horizon_band_includes_zero}`],
      ],
      colw: [5400, 3960],
    }];
  },
  "3": () => {
    const rc = readCsv(TAB("t03_regime_coupling.csv"));
    const fz = readCsv(TAB("t03_fisher_pairwise.csv"));
    return [{
      headers: ["Phase", "Days", "n", "r", "95% CI", "p"],
      rows: rc.map((r) => r.pearson_r === "" ? [r.phase, dash(r.days), r.n, "—", "—", "not estimable (no strikes)"]
        : [r.phase, dash(r.days), r.n, fix(r.pearson_r, 2), `${fix(r.ci95_low, 2)} to ${fix(r.ci95_high, 2)}`, pfmt(r.p_value)]),
      colw: [1700, 1100, 700, 900, 2200, 2760],
    }, {
      headers: ["Comparison", "z", "p", "Holm p"],
      rows: fz.map((r) => [r.comparison.replace("Major ", "").replace("First ", ""), fix(r.z, 2), pfmt(r.p_raw), pfmt(r.p_holm)]),
      colw: [3600, 1600, 2000, 2160],
    }];
  },
  "4": () => {
    const fe = readCsv(TAB("t04_fevd_orderings.csv"));
    const sh = (ordStart, variable, shock) => pct(rowWhere(fe, (r) => r.ordering.startsWith(ordStart) && r.variable === variable && r.shock_source === shock).share_h12);
    return [{
      headers: ["Ordering assumption", "Strike shocks → share of retaliation variance", "Retaliation shocks → share of strike variance"],
      rows: [
        ["Strikes first, then retaliation", sh("strikes first", "retal", "strikes"), sh("strikes first", "strikes", "retal")],
        ["Retaliation first, then strikes", sh("retaliation first", "retal", "strikes"), sh("retaliation first", "strikes", "retal")],
      ],
      colw: [3160, 3100, 3100],
    }];
  },
  "5": () => {
    const ra = readCsv(TAB("t05_ratio_by_phase.csv"));
    return [{
      headers: ["Phase", "Strikes/day", "Retaliation/day", "Ratio (bootstrap 95% CI)", "Strikes lead (+1 day)", "Retaliation leads (+1 day)"],
      rows: ra.map((r) => {
        const active = Number(r.strikes_total) > 0;
        return [r.phase, fix(r.strikes_per_day, 2), fix(r.retal_per_day, 2),
          active ? `${fix(r.strike_retal_ratio, 2)} (${fix(r.ratio_ci95_low, 2)} to ${fix(r.ratio_ci95_high, 2)})` : fix(r.strike_retal_ratio, 2),
          active ? fix(r.ccf_strikes_lead_1d, 2) : "—", active ? fix(r.ccf_retal_lead_1d, 2) : "—"];
      }),
      colw: [1600, 1100, 1300, 2260, 1500, 1600],
    }];
  },
  "6": () => {
    const wk = readCsv(TAB("t06_weekly.csv"))[0];
    const nW = readCsv(TAB("t06_weekly.csv")).length;
    const g = readCsv(TAB("t06_granger.csv"));
    const dp = readCsv(TAB("t06_diplomacy_phase.csv"));
    const kw = readCsv(TAB("t06_regime_test.csv"))[0];
    const gr = (dir) => { const r = rowWhere(g, (x) => x.direction === dir); return `F = ${fix(r.F, 2)}, ${pstr(r.p_value)}`; };
    return [{
      headers: ["Quantity", "Value"],
      rows: [
        [`Weekly Pearson r, violence vs diplomacy (n = ${nW} weeks)`, `${fix(wk.pearson_r_all_weeks, 2)} (${pstr(wk.p_all_weeks)})`],
        ["Weekly Spearman rho", `${fix(wk.spearman_rho_all_weeks, 2)} (${pstr(wk.p_spearman)})`],
        [`Granger, violence → diplomacy (lag ${g[0].lag})`, gr("violence -> diplomatic")],
        [`Granger, diplomacy → violence (lag ${g[1].lag})`, gr("diplomatic -> violence")],
        ["Diplomatic events/day: Combat / Ceasefire / Resumption / Pause", dp.map((r) => fix(r.diplomatic_per_day, 2)).join(" / ")],
        ["Share of days with any diplomacy: Combat / Ceasefire / Resumption / Pause", dp.map((r) => fix(r.share_days_with_diplomacy, 2)).join(" / ")],
        ["Kruskal–Wallis across phases, diplomatic events/day", `H(3) = ${fix(kw.H, 1)}, ${pstr(kw.p_value)}, ε² = ${fix(kw.epsilon_squared, 2)}`],
      ],
      colw: [5400, 3960],
    }];
  },
  "7": () => {
    const bs = readCsv(TAB("t07_break_selection.csv"));
    const pl = readCsv(TAB("t07_placebo_summary.csv"));
    const obs = fix(pl[0].observed_bic_gain, 1);
    const label = (s) => s.startsWith("shuffled") ? "Shuffled days (no time structure)"
      : s.includes("within-regime") ? `AR(1), within-regime autocorrelation ${s.match(/phi=([0-9.]+)/)[1]}`
      : `AR(1), whole-series autocorrelation ${s.match(/phi=([0-9.]+)/)[1]}`;
    return [{
      headers: ["Number of segments", "Break days", "BIC"],
      rows: bs.map((r) => [r.n_segments, r.break_days ? r.break_days.split(",").join(", ") : "—", fix(r.bic, 1)]),
      colw: [2600, 4200, 2560],
    }, {
      headers: ["Placebo null (1,000 draws each)", "Share choosing 6 segments", "Median BIC gain", "Maximum BIC gain", `p (gain ≥ observed ${obs})`],
      // order: least to most conservative null (shuffle, within-regime AR(1), whole-series AR(1))
      rows: [pl.find((r) => r.null.startsWith("shuffled")), pl.find((r) => r.null.includes("within-regime")), pl.find((r) => r.null.includes("whole-series"))]
        .map((r) => [label(r.null), fix(r.share_selecting_k6, 2), fix(r.median_bic_gain, 1), fix(r.max_bic_gain, 1), fix(r.p_value_gain_ge_observed, 3)]),
      colw: [3360, 1500, 1500, 1500, 1500],
    }];
  },
  "8": () => {
    const rs = readCsv(TAB("t08_resumption.csv"));
    const fs_ = readCsv(TAB("t08_full_sample.csv"));
    const cellOf = (r) => `F${r.df} = ${fix(r.F, 2)}, ${pstr(r.p_value)}`;
    const pair = (rows, pred) => [cellOf(rowWhere(rows, (r) => pred(r) && r.direction === "retal -> strikes")),
                                  cellOf(rowWhere(rows, (r) => pred(r) && r.direction === "strikes -> retal"))];
    const n = rs[0].n_obs_used;
    return [{
      headers: ["Sample and specification", "Retaliation → strikes", "Strikes → retaliation"],
      rows: [
        [`Resumption, primary measure, lag 1 (${n} obs.)`, ...pair(rs, (r) => r.measure.startsWith("primary"))],
        [`Resumption, raw event records, lag 1 (${n} obs.)`, ...pair(rs, (r) => r.measure.startsWith("raw"))],
        ["Full sample, levels, AIC lag 9 (parent draft)", ...pair(fs_, (r) => r.sample.startsWith("Full sample, naive") && r.lag_criterion.startsWith("AIC"))],
        ["Full sample, four phase means removed, lag 1 (HQIC; BIC selects 0)", ...pair(fs_, (r) => r.sample.includes("(4 documented") && r.lag_criterion.startsWith("HQIC"))],
        ["Full sample, four phase means removed, AIC lag 4", ...pair(fs_, (r) => r.sample.includes("(4 documented") && r.lag_criterion.startsWith("AIC"))],
        ["Full sample, six detected regime means removed, lag 1", ...pair(fs_, (r) => r.sample.includes("(6 detected") && r.lag_criterion.startsWith("BIC"))],
        ["Full sample, six detected regime means removed, AIC lag 4", ...pair(fs_, (r) => r.sample.includes("(6 detected") && r.lag_criterion.startsWith("AIC"))],
      ],
      colw: [4160, 2600, 2600],
    }];
  },
  "9": () => {
    const op = readCsv(TAB("t09_operationalization.csv"));
    const cm = readCsv(TAB("t09_countmodel_retal.csv"));
    const st = readCsv(TAB("t09_stationarity.csv"));
    const cp = readCsv(TAB("t09_casualty_propagation.csv"));
    const r3 = (sample) => op.filter((r) => r.sample.startsWith(sample)).map((r) => fix(r.same_day_r, 2)).join(" / ");
    const nb = (term) => rowWhere(cm, (r) => r.sample.startsWith("full") && r.term === term);
    const adf = (series) => rowWhere(st, (r) => r.sample.startsWith("combat") && r.series === series).adf_p;
    const adfp = (p) => Number(p) < 0.001 ? fix(p, 4) : fix(p, 3);
    const combatLagged = cm.filter((r) => r.sample.startsWith("combat") && /strikes_L[12]/.test(r.term)).every((r) => Number(r.p_value) > 0.05);
    const cpmin = Math.min(...cp.filter((r) => r.sample.startsWith("combat")).map((r) => Number(r.p_value)));
    return [{
      headers: ["Check", "Result"],
      rows: [
        ["Same-day r, combat: distinct locations / raw records / timeline-only", `${r3("combat")} (all p < 0.05)`],
        ["Same-day r, full sample: distinct locations / raw records / timeline-only", `${r3("full")} (all p < 0.001)`],
        ["Negative binomial, full sample: same-day strikes IRR (p)", `${fix(nb("strikes_L0").IRR, 2)} (${pfmt(nb("strikes_L0").p_value)})`],
        ["Negative binomial, full sample: lagged retaliation IRR (p)", `${fix(nb("retal_L1").IRR, 2)} (${pfmt(nb("retal_L1").p_value)})`],
        ["Negative binomial, combat: lagged strikes (1 and 2 days)", combatLagged ? "not significant" : "significant"],
        ["ADF within combat: strikes / retaliation", `p = ${adfp(adf("strikes"))} / p = ${adfp(adf("retal"))} (unit root rejected)`],
        ["KPSS full sample: every series", st.filter((r) => r.sample.startsWith("full")).every((r) => r.kpss_rejects_stationarity === "True") ? "stationarity rejected (regime mean shifts)" : "mixed"],
        ["Deaths on tempo, combat, all lags", `not significant (minimum p = ${fix(cpmin, 2)})`],
      ],
      colw: [5400, 3960],
    }];
  },
  "A1": () => {
    const txt = fs.readFileSync(TAB("t02_var_combat_summary.txt"), "utf8");
    const rows = [];
    let eq = null;
    for (const line of txt.split(/\r?\n/)) {
      const m = line.match(/^Results for equation (\w+)/);
      if (m) { eq = m[1] === "strikes" ? "Strikes" : "Retaliation"; continue; }
      const c = line.match(/^(const|L1\.strikes|L1\.retal)\s+(-?[\d.]+)\s+([\d.]+)\s+(-?[\d.]+)\s+([\d.]+)/);
      if (c && eq) {
        const term = { "const": "constant", "L1.strikes": "strikes, lag 1", "L1.retal": "retaliation, lag 1" }[c[1]];
        rows.push([eq, term, fix(c[2], 2), fix(c[3], 2), Number(c[5]) < 0.1 ? fix(c[5], 3) : fix(c[5], 2)]);
      }
    }
    if (rows.length !== 6) throw new Error("could not parse VAR summary");
    return [{ headers: ["Equation", "Term", "Coefficient", "SE", "p"], rows, colw: [1900, 2600, 1700, 1500, 1660] }];
  },
};

// --------------------------------------------- markdown parsing + guard --
const md = fs.readFileSync(MD, "utf8").split(/\r?\n/);

function parseMdTable(lines, start) {
  // returns {rows, next}: rows = array of arrays of cell strings (header first), skipping the |---| rule
  const rows = [];
  let i = start;
  while (i < lines.length && lines[i].trim().startsWith("|")) {
    const cells = lines[i].trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
    if (!cells.every((c) => /^:?-+:?$/.test(c))) rows.push(cells);
    i++;
  }
  return { rows, next: i };
}

function guardTable(num, k, mdRows, built) {
  const bRows = [built.headers, ...built.rows];
  if (bRows.length !== mdRows.length) throw new Error(`Table ${num} (part ${k + 1}): ${bRows.length} rows built vs ${mdRows.length} in markdown`);
  for (let r = 0; r < bRows.length; r++) {
    if (bRows[r].length !== mdRows[r].length) throw new Error(`Table ${num} row ${r}: column count differs`);
    for (let c = 0; c < bRows[r].length; c++) {
      const a = plain(String(bRows[r][c])).trim(), b = plain(mdRows[r][c]).trim();
      if (a !== b) throw new Error(`Table ${num} row ${r} col ${c}: built "${a}" vs markdown "${b}"`);
    }
  }
}

const FIGS = { "1": "fig1_trajectory.png", "2": "fig2_same_day.png", "3": "fig3_regime_coupling.png",
  "4": "fig4_identification.png", "5": "fig5_asymmetry_spread.png", "6": "fig6_diplomacy.png",
  "7": "fig7_breaks_placebo.png", "A1": "figA1_irf_combat.png" };
const sizePng = (buf) => ({ w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) });
function figure(num) {
  const data = fs.readFileSync(FIG(FIGS[num]));
  const { w, h } = sizePng(data);
  const W = 624;
  return new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 120, after: 120 },
    children: [new ImageRun({ data, type: "png", transformation: { width: W, height: Math.round((h / w) * W) } })],
  });
}

// ------------------------------------------------------------- build --
const children = [];
let i = 0;
let title = "", meta = [];
// title block: first "# " line, then lines until "## Abstract"
while (i < md.length && !md[i].startsWith("# ")) i++;
title = md[i].replace(/^# /, "").trim(); i++;
while (i < md.length && !md[i].startsWith("## Abstract")) { if (md[i].trim() && md[i].trim() !== "---") meta.push(md[i].trim()); i++; }

// --- title page (APA professional) ---
children.push(new Paragraph({ spacing: { before: 2400 } }));
children.push(new Paragraph({ children: [new TextRun({ text: title, bold: true, font: FONT, size: BODY })],
  alignment: AlignmentType.CENTER, spacing: { line: DOUBLE, after: 240 } }));
const authorsLine = meta.find((l) => /^Jacob/.test(l)) || "";
const authors = authorsLine.split(" and ").map((s) => s.trim());
// a bracketed placeholder such as "[Co-author: name, affiliation]" renders as "[Co-author]" / "[Affiliation]"
const names = authors.map((a) => a.startsWith("[") ? "[Co-author]" : a.replace(/\s*\(.*\)\s*$/, ""));
const affils = authors.map((a) => { const m = a.match(/\((.*)\)/); return (m && !a.startsWith("[")) ? m[1] : "[Affiliation]"; });
children.push(new Paragraph({ children: [new TextRun({ text: `${names[0]}¹ and ${names[1] || "[Co-author]"}²`, font: FONT, size: BODY })],
  alignment: AlignmentType.CENTER, spacing: { line: DOUBLE, after: 0 } }));
children.push(new Paragraph({ children: [new TextRun({ text: `¹ ${affils[0]}`, font: FONT, size: BODY })], alignment: AlignmentType.CENTER, spacing: { line: DOUBLE, after: 0 } }));
children.push(new Paragraph({ children: [new TextRun({ text: `² ${affils[1] || "[Affiliation]"}`, font: FONT, size: BODY })], alignment: AlignmentType.CENTER, spacing: { line: DOUBLE, after: 480 } }));
children.push(new Paragraph({ children: [new TextRun({ text: "Author Note", bold: true, font: FONT, size: BODY })], alignment: AlignmentType.CENTER, spacing: { line: DOUBLE, before: 1200, after: 0 } }));
for (const l of meta.filter((l) => l.startsWith("*") || l.startsWith("**"))) {
  const t = plain(l).replace(/^Major Revision 1 — /, "Major Revision 1 of ");
  children.push(new Paragraph({ children: runs(t), spacing: { line: DOUBLE, after: 0 }, indent: { firstLine: 720 }, alignment: AlignmentType.LEFT }));
}
children.push(new Paragraph({ children: runs("Correspondence concerning this article should be addressed to Jacob E. Thomas, Results Generation, Austin, Texas. Repository: github.com/jethomasphd/WarTheater."),
  spacing: { line: DOUBLE, after: 0 }, indent: { firstLine: 720 } }));
children.push(pageBreak());

// --- walk the rest ---
let inReferences = false;
let pendingTable = null;   // table number whose md table(s) we are about to consume
let tablePart = 0;
while (i < md.length) {
  const line = md[i];
  const t = line.trim();
  if (!t || t === "---") { i++; continue; }

  if (t.startsWith("## ")) {
    const h = t.replace(/^## /, "");
    inReferences = /^References/.test(h);
    if (/^Abstract/.test(h)) {
      children.push(h1("Abstract"));
      // abstract paragraph(s) with no indent, then keywords
      i++;
      while (i < md.length && !md[i].startsWith("## ")) {
        const s = md[i].trim();
        if (s && s !== "---") {
          if (s.startsWith("**Keywords:**")) {
            children.push(new Paragraph({ children: [new TextRun({ text: "Keywords: ", italics: true, font: FONT, size: BODY }), ...runs(s.replace("**Keywords:**", "").trim())],
              spacing: { line: DOUBLE, after: 0 }, indent: { firstLine: 720 } }));
          } else children.push(noIndent(s));
        }
        i++;
      }
      children.push(pageBreak());
      continue;
    }
    if (/^References/.test(h) || /^Appendix/.test(h)) children.push(pageBreak());
    children.push(h1(h.replace(/^\d+\.\s*/, (m) => m)));  // keep numbering as written
    i++; continue;
  }
  if (t.startsWith("### ")) { children.push(h2(t.replace(/^### /, ""))); i++; continue; }

  if (t.startsWith("**Table ")) {
    const m = t.match(/^\*\*Table ([A-Z]?\d+)\.\*\*\s*\*(.*)\*\s*$/);
    if (!m) throw new Error(`bad table caption: ${t}`);
    pendingTable = m[1]; tablePart = 0;
    children.push(...caption(`Table ${m[1]}`, m[2]));
    i++; continue;
  }
  if (t.startsWith("|")) {
    const { rows, next } = parseMdTable(md, i);
    if (!pendingTable) throw new Error(`markdown table without a Table caption at line ${i + 1}`);
    const built = TABLES[pendingTable]();
    if (tablePart >= built.length) throw new Error(`Table ${pendingTable}: more markdown tables than built parts`);
    guardTable(pendingTable, tablePart, rows, built[tablePart]);
    children.push(apaTable(built[tablePart].headers, built[tablePart].rows, built[tablePart].colw));
    children.push(new Paragraph({ spacing: { after: 120 } }));
    tablePart++;
    i = next; continue;
  }
  if (t.startsWith("*Note.*")) { children.push(note(t.replace(/^\*Note\.\*\s*/, ""))); pendingTable = null; i++; continue; }

  if (t.startsWith("**Figure ")) {
    const m = t.match(/^\*\*Figure ([A-Z]?\d+)\.\*\*\s*\*(.*?)\*\s*(.*)$/);
    if (!m) throw new Error(`bad figure caption: ${t}`);
    children.push(...caption(`Figure ${m[1]}`, m[2]));
    children.push(figure(m[1]));
    if (m[3].trim()) children.push(note(m[3].trim()));
    i++; continue;
  }
  if (t.startsWith("- ")) {
    if (inReferences) {
      children.push(new Paragraph({ children: runs(t.slice(2)), spacing: { line: DOUBLE, after: 0 },
        indent: { left: 720, hanging: 720 }, alignment: AlignmentType.LEFT }));
    } else children.push(bullet(t.slice(2)));
    i++; continue;
  }
  if (/^\*\[.*\]\*$/.test(t)) {   // italic bracketed convention notes
    children.push(noIndent(t.slice(1, -1), { italics: true }));
    i++; continue;
  }
  // paragraph (may span multiple lines until blank)
  let para = [t]; i++;
  while (i < md.length && md[i].trim() && !/^(#|\||\*\*Table|\*\*Figure|\*Note\.|- |---)/.test(md[i].trim())) { para.push(md[i].trim()); i++; }
  children.push(body(para.join(" ")));
}

// ----------------------------------------------------------------- doc --
const header = new Header({ children: [new Paragraph({
  tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
  children: [new TextRun({ text: RUNNING_HEAD, font: FONT, size: BODY }), new TextRun({ text: "\t", font: FONT, size: BODY }),
    new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: BODY })],
})] });

const doc = new Document({
  creator: "IranWar.ai research series — Paper 1 Major Revision 1",
  title,
  styles: {
    default: { document: { run: { font: FONT, size: BODY } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: BODY, bold: true, color: "000000" }, paragraph: { alignment: AlignmentType.CENTER, spacing: { line: DOUBLE, before: 240 } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: BODY, bold: true, color: "000000" }, paragraph: { spacing: { line: DOUBLE, before: 120 } } },
    ],
  },
  numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    headers: { default: header },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("wrote", OUT, `(${(buf.length / 1024).toFixed(0)} KB)`);
});
