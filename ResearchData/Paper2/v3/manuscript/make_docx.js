#!/usr/bin/env node
/**
 * Paper 2 — v3: build the Word manuscript from paper2_v3.md.
 *
 *   cd manuscript && node make_docx.js
 *
 * Needs the `docx` npm package. Either `npm install docx` inside this
 * directory, or point NODE_PATH at a directory that contains node_modules/docx.
 *
 * What it does
 * ------------
 * Reads paper2_v3.md (the canonical text) and writes paper2_v3.docx next to
 * it. The markdown is rendered generically: headings, paragraphs, bullet and
 * numbered lists, blockquote drafting notes (rendered as shaded boxes),
 * tables, figures (PNG files under ../output/figures/), and code blocks.
 * The tables in the markdown are themselves rendered from the result CSVs
 * and checked verbatim by src/06_manuscript_tables.py, so the Word file
 * cannot drift from the analysis. Inline **bold**, *italic*, and `code`
 * are honoured. Nothing here re-computes any number.
 */
const fs = require("fs");
const path = require("path");
const {
  AlignmentType, BorderStyle, Document, Footer, HeadingLevel, ImageRun,
  LevelFormat, PageNumber, Packer, Paragraph, ShadingType, Table, TableCell,
  TableRow, TextRun, WidthType,
} = require("docx");

const HERE = __dirname;
const MD = path.join(HERE, "paper2_v3.md");
const OUT = path.join(HERE, "paper2_v3.docx");
const FONT = "Georgia";
const MONO = "Consolas";
const BODY = 21;          // half-points (10.5 pt)
const SMALL = 18;         // 9 pt
const TABLE = 15;         // 7.5 pt
const PAGE_W = 9360;      // 6.5 in text width in DXA

// ------------------------------------------------------------ inline runs --
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const tok = m[0];
    if (tok.startsWith("**")) out.push(new TextRun({ text: tok.slice(2, -2), bold: true, ...base }));
    else if (tok.startsWith("`")) out.push(new TextRun({ text: tok.slice(1, -1), font: MONO, size: (base.size || BODY) - 2, ...base }));
    else out.push(new TextRun({ text: tok.slice(1, -1), italics: true, ...base }));
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}

const P = (text, opts = {}, base = {}) => new Paragraph({
  children: runs(text, base), spacing: { after: 140, line: 264 },
  alignment: AlignmentType.LEFT, ...opts,
});

// --------------------------------------------------------------- figures --
const sizePng = (buf) => ({ w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) });
function figure(relPath) {
  const file = path.resolve(HERE, relPath);
  const data = fs.readFileSync(file);
  const { w, h } = sizePng(data);
  const W = 624;   // 6.5 in at 96 px/in
  return new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 120, after: 200 },
    children: [new ImageRun({ data, type: "png", transformation: { width: W, height: Math.round((h / w) * W) } })],
  });
}

// ---------------------------------------------------------------- tables --
function parseTable(lines) {
  const rowsRaw = lines.filter((l) => !/^\|\s*-{2,}/.test(l));
  const rows = rowsRaw.map((l) => l.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim()));
  return { header: rows[0], body: rows.slice(1) };
}
function tableBlock({ header, body }) {
  const n = header.length;
  // Column widths proportional to the longest cell in each column (capped), min width for narrow columns.
  const lens = header.map((h, i) => Math.min(40, Math.max(h.length, ...body.map((r) => (r[i] || "").length))));
  const total = lens.reduce((a, b) => a + b, 0);
  let widths = lens.map((l) => Math.max(700, Math.round((l / total) * PAGE_W)));
  const sum = widths.reduce((a, b) => a + b, 0);
  widths = widths.map((w) => Math.round((w / sum) * PAGE_W));
  widths[n - 1] += PAGE_W - widths.reduce((a, b) => a + b, 0);   // make the widths sum exactly
  const cell = (t, i, head) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    shading: head ? { type: ShadingType.CLEAR, fill: "EDF2F7" } : undefined,
    margins: { top: 30, bottom: 30, left: 60, right: 60 },
    children: [new Paragraph({
      alignment: i === 0 ? AlignmentType.LEFT : AlignmentType.LEFT,
      spacing: { after: 0, line: 240 },
      children: runs(t, { size: TABLE, bold: head }),
    })],
  });
  return new Table({
    width: { size: PAGE_W, type: WidthType.DXA }, columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, children: header.map((t, i) => cell(t, i, true)) }),
      ...body.map((r) => new TableRow({ children: header.map((_, i) => cell(r[i] || "", i, false)) })),
    ],
  });
}

// ------------------------------------------------------------ note boxes --
function noteParagraphs(texts) {
  return texts.map((t, k) => new Paragraph({
    style: "DraftingNote",
    children: runs(t, { size: SMALL, color: "3A2E00" }),
    spacing: { before: k === 0 ? 120 : 40, after: k === texts.length - 1 ? 200 : 40, line: 252 },
    indent: { left: 240, right: 240 },
    shading: { type: ShadingType.CLEAR, fill: "FFF6DD" },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: "E69F00", space: 6 } },
  }));
}

// ------------------------------------------------------------- markdown --
const md = fs.readFileSync(MD, "utf8").split("\n");
const children = [];
let listInstance = 0;
let i = 0;
let titleDone = false;
let inFrontMatter = true;   // lines between the title and the first '---' are the title block

function flushParagraph(buf) {
  if (!buf.length) return;
  const text = buf.join(" ").trim();
  if (!text) return;
  if (/^\*\*Table \d+\./.test(text)) {
    children.push(new Paragraph({ children: runs(text, { size: SMALL }), spacing: { before: 200, after: 80 }, keepNext: true }));
  } else if (/^\*\*Figure \d+\./.test(text)) {
    children.push(new Paragraph({ children: runs(text, { size: SMALL, color: "333333" }), spacing: { before: 160, after: 60 }, keepNext: true }));
  } else if (/^\*How to read/.test(text)) {
    children.push(new Paragraph({ children: runs(text, { size: SMALL, color: "333333" }), spacing: { before: 60, after: 200, line: 252 }, indent: { left: 240 } }));
  } else if (inFrontMatter) {
    children.push(new Paragraph({ children: runs(text, { size: 19, color: "444444" }), alignment: AlignmentType.CENTER, spacing: { after: 100 } }));
  } else {
    children.push(P(text));
  }
}

let buf = [];
while (i < md.length) {
  const line = md[i];

  if (!titleDone && line.startsWith("# ")) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 600, after: 240 },
      children: runs(line.slice(2).trim(), { size: 34, bold: true }),
    }));
    titleDone = true; i++; continue;
  }
  if (line.trim() === "---") {
    flushParagraph(buf); buf = [];
    if (inFrontMatter) inFrontMatter = false;
    else children.push(new Paragraph({ spacing: { before: 60, after: 60 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "BBBBBB", space: 1 } }, children: [] }));
    i++; continue;
  }
  if (line.startsWith("## ")) {
    flushParagraph(buf); buf = []; inFrontMatter = false;
    children.push(new Paragraph({ text: line.slice(3).trim(), heading: HeadingLevel.HEADING_1, spacing: { before: 320, after: 140 } }));
    i++; continue;
  }
  if (line.startsWith("### ")) {
    flushParagraph(buf); buf = [];
    children.push(new Paragraph({ text: line.slice(4).trim(), heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 100 } }));
    i++; continue;
  }
  if (line.startsWith(">")) {
    flushParagraph(buf); buf = [];
    const paras = []; let cur = [];
    while (i < md.length && md[i].startsWith(">")) {
      const t = md[i].replace(/^>\s?/, "");
      if (t.trim() === "") { if (cur.length) { paras.push(cur.join(" ")); cur = []; } }
      else cur.push(t.trim());
      i++;
    }
    if (cur.length) paras.push(cur.join(" "));
    children.push(...noteParagraphs(paras));
    continue;
  }
  if (line.startsWith("|")) {
    flushParagraph(buf); buf = [];
    const tl = [];
    while (i < md.length && md[i].startsWith("|")) { tl.push(md[i]); i++; }
    children.push(tableBlock(parseTable(tl)));
    children.push(new Paragraph({ spacing: { after: 60 }, children: [] }));
    continue;
  }
  if (line.startsWith("![")) {
    flushParagraph(buf); buf = [];
    const m = line.match(/\((.*?)\)/);
    children.push(figure(m[1]));
    i++; continue;
  }
  if (line.startsWith("```")) {
    flushParagraph(buf); buf = [];
    i++;
    while (i < md.length && !md[i].startsWith("```")) {
      children.push(new Paragraph({
        children: [new TextRun({ text: md[i], font: MONO, size: 17 })],
        spacing: { after: 0, line: 240 }, indent: { left: 240 },
        shading: { type: ShadingType.CLEAR, fill: "F4F4F4" },
      }));
      i++;
    }
    children.push(new Paragraph({ spacing: { after: 140 }, children: [] }));
    i++; continue;
  }
  const bullet = line.match(/^- (.*)$/);
  const number = line.match(/^(\d+)\. (.*)$/);
  if (bullet || number) {
    flushParagraph(buf); buf = [];
    listInstance += 1;
    const isNum = !!number;
    while (i < md.length) {
      const b = md[i].match(/^- (.*)$/), n = md[i].match(/^(\d+)\. (.*)$/);
      if (!(isNum ? n : b)) break;
      let text = (isNum ? n[2] : b[1]).trim();
      i++;
      while (i < md.length && md[i].startsWith("  ") && md[i].trim()) { text += " " + md[i].trim(); i++; }
      children.push(new Paragraph({
        children: runs(text), spacing: { after: 80, line: 264 },
        numbering: { reference: isNum ? "numbers" : "bullets", level: 0, instance: listInstance },
      }));
    }
    continue;
  }
  if (line.trim() === "") { flushParagraph(buf); buf = []; i++; continue; }
  buf.push(line.trim());
  i++;
}
flushParagraph(buf);

// ------------------------------------------------------------------- doc --
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
      { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] },
    ],
  },
  styles: {
    default: {
      document: { run: { font: FONT, size: BODY } },
      heading1: { run: { font: FONT, size: 27, bold: true, color: "1A1A1A" } },
      heading2: { run: { font: FONT, size: 23, bold: true, color: "1A1A1A" } },
    },
    paragraphStyles: [
      // Every drafting note carries this named style, so they can be found (and deleted) in Word with one search.
      { id: "DraftingNote", name: "Drafting Note", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: SMALL, color: "3A2E00" } },
    ],
  },
  sections: [{
    properties: {
      page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } },
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "IranWar.ai Research Agenda — Paper 2, version 3 (drafting document) — page ", size: 16, color: "666666" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "666666" }),
          ],
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("wrote", path.relative(process.cwd(), OUT), `(${(buf.length / 1024).toFixed(0)} KB)`);
});
