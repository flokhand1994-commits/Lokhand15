// Flashcard export, shared by every flashcard page.
// ExportCards.button(getData) returns an "⬇ Export" button with three choices:
//   • Printable flashcards — a grid of cards to print double-sided (or save as PDF)
//   • Spreadsheet (.csv) — opens in Excel, Numbers or Google Sheets
//   • Anki / Quizlet (.txt) — one card per line: front <tab> back
// getData() returns {name, header: [...], rows: [[...]], front(row), back(row)};
// back(row) is "meaning | example = translation | …", and printRows optionally
// limits what gets printed.
(function () {
  const css = `
.xp{position:relative;display:inline-block}
.xp-btn{padding:7px 14px;border:1.5px solid #c8d8e8;border-radius:8px;background:#fff;color:#2c6aa0;font:inherit;font-size:.88rem;font-weight:600;cursor:pointer;min-height:44px}
.xp-btn:hover{background:#2c6aa0;color:#fff}
.xp-menu{position:absolute;right:0;top:calc(100% + 6px);z-index:50;background:#fff;border:1px solid #c8d8e8;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.12);padding:6px;min-width:230px;display:none;text-align:left}
.xp.open .xp-menu{display:block}
.xp-menu button{display:block;width:100%;text-align:left;border:none;background:none;padding:10px 12px;border-radius:8px;font:inherit;font-size:.88rem;color:#1a2b3c;cursor:pointer}
.xp-menu button:hover{background:#eef4fa}
.xp-menu small{display:block;color:#5a6b7c;font-size:.74rem;margin-top:2px}`;
  const style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  const clean = v => String(v == null ? '' : v).replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
  const csvCell = v => /[",\n;]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v;
  const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

  function download(filename, text, type) {
    const blob = new Blob(['﻿' + text], {type: `${type};charset=utf-8`});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  function toCsv(d) {
    return [d.header, ...d.rows].map(r => r.map(v => csvCell(clean(v))).join(',')).join('\r\n');
  }

  function toCards(d) {
    return d.rows.map(r => `${clean(d.front(r)).replace(/\t/g, ' ')}\t${clean(d.back(r)).replace(/\t/g, ' ')}`).join('\n');
  }

  const esc = s => clean(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const PER_PAGE = 8, COLS = 2;

  // Printable cards: a grid of fronts (words), then a page of backs (meaning and
  // translations) mirrored left-to-right, so each back lands behind its word when
  // printed double-sided ("flip on long edge").
  function printCards(d) {
    const rows = d.printRows || d.rows;
    const front = r => {
      const f = clean(d.front(r));
      const m = f.match(/^(.*?) \((.*)\)$/);          // "하다 (hada)" → word + pronunciation
      return m ? `<div class="w">${esc(m[1])}</div><div class="r">${esc(m[2])}</div>` : `<div class="w">${esc(f)}</div>`;
    };
    const back = r => {
      const [meaning, ...rest] = clean(d.back(r)).split(' | ');
      const lines = rest.map(x => {
        const [tl, tr] = x.split(' = ');
        return tr ? `<div class="ex"><b>${esc(tl)}</b><span>${esc(tr)}</span></div>` : `<div class="ex"><span>${esc(tl)}</span></div>`;
      });
      return `<div class="m">${esc(meaning)}</div>${lines.join('')}`;
    };
    let pages = '';
    for (let i = 0; i < rows.length; i += PER_PAGE) {
      const chunk = rows.slice(i, i + PER_PAGE);
      while (chunk.length < PER_PAGE) chunk.push(null);
      const fronts = chunk.map((r, k) => `<div class="card f">${r ? `<span class="n">${i + k + 1}</span>${front(r)}` : ''}</div>`);
      const backs = [];
      for (let k = 0; k < PER_PAGE; k += COLS) {
        backs.push(...chunk.slice(k, k + COLS).reverse().map(r => `<div class="card b">${r ? back(r) : ''}</div>`));
      }
      pages += `<section class="sheet">${fronts.join('')}</section><section class="sheet">${backs.join('')}</section>`;
    }
    const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(d.name)} — printable flashcards</title>
<style>
@page{size:A4;margin:10mm}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#1a2b3c;background:#f4f7fb}
.bar{position:sticky;top:0;z-index:2;background:#fff;border-bottom:1px solid #c8d8e8;padding:12px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;font-size:.88rem;color:#5a6b7c}
.bar button{padding:9px 16px;border:none;border-radius:8px;background:#2c6aa0;color:#fff;font:inherit;font-weight:600;cursor:pointer}
.bar b{color:#1a2b3c}
.sheet{width:190mm;height:277mm;margin:12px auto;background:#fff;display:grid;grid-template-columns:repeat(${COLS},1fr);grid-template-rows:repeat(${PER_PAGE / COLS},1fr);box-shadow:0 2px 10px rgba(0,0,0,.08);page-break-after:always;break-after:page}
.card{border:.3mm dashed #b8c4d0;padding:6mm;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;position:relative;overflow:hidden}
.n{position:absolute;top:3mm;left:4mm;font-size:8pt;color:#9aa8b6}
.f .w{font-size:22pt;font-weight:700;color:#2c6aa0;line-height:1.2}
.f .r{font-size:11pt;color:#5a6b7c;font-style:italic;margin-top:2mm}
.b .m{font-size:15pt;font-weight:700;margin-bottom:3mm;line-height:1.3}
.b .ex{font-size:10pt;line-height:1.35;margin-top:2mm}
.b .ex b{display:block;font-weight:600}
.b .ex span{display:block;color:#5a6b7c}
@media print{body{background:#fff}.bar{display:none}.sheet{margin:0;box-shadow:none}}
@media screen and (max-width:800px){.sheet{zoom:.45}}
</style></head><body>
<div class="bar"><button onclick="print()">🖨 Print / Save as PDF</button>
<span><b>${rows.length} cards</b> · Print double-sided (flip on long edge), then cut along the dashed lines.</span></div>
${pages}
</body></html>`;
    const w = window.open('', '_blank');
    if (!w) { alert('Please allow pop-ups for this site to open the printable cards.'); return; }
    w.document.open();
    w.document.write(html);
    w.document.close();
  }

  window.ExportCards = {
    button(getData) {
      const wrap = document.createElement('div');
      wrap.className = 'xp';
      wrap.innerHTML = `<button type="button" class="xp-btn" aria-haspopup="true">⬇ Export</button>
        <div class="xp-menu" role="menu">
          <button type="button" data-f="print" role="menuitem">Printable flashcards (PDF)<small>Words on the front, meaning on the back — print or save as PDF</small></button>
          <button type="button" data-f="csv" role="menuitem">Spreadsheet (.csv)<small>Excel, Numbers, Google Sheets</small></button>
          <button type="button" data-f="cards" role="menuitem">Anki / Quizlet (.txt)<small>Front and back, ready to import</small></button>
        </div>`;
      wrap.querySelector('.xp-btn').addEventListener('click', e => { e.stopPropagation(); wrap.classList.toggle('open'); });
      document.addEventListener('click', () => wrap.classList.remove('open'));
      wrap.querySelectorAll('[data-f]').forEach(b => b.addEventListener('click', e => {
        e.stopPropagation();
        wrap.classList.remove('open');
        const d = getData();
        if (b.dataset.f === 'print') printCards(d);
        else if (b.dataset.f === 'csv') download(`${slug(d.name)}.csv`, toCsv(d), 'text/csv');
        else download(`${slug(d.name)}-flashcards.txt`, toCards(d), 'text/plain');
      }));
      return wrap;
    },
  };
})();
