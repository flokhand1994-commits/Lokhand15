// Flashcard export, shared by every flashcard page.
// ExportCards.button(getData) returns an "⬇ Export" button with two choices:
//   • Spreadsheet (.csv) — opens in Excel, Numbers or Google Sheets
//   • Anki / Quizlet (.txt) — one card per line: front <tab> back
// getData() returns {name, header: [...], rows: [[...]], front(row), back(row)}.
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

  window.ExportCards = {
    button(getData) {
      const wrap = document.createElement('div');
      wrap.className = 'xp';
      wrap.innerHTML = `<button type="button" class="xp-btn" aria-haspopup="true">⬇ Export</button>
        <div class="xp-menu" role="menu">
          <button type="button" data-f="csv" role="menuitem">Spreadsheet (.csv)<small>Excel, Numbers, Google Sheets</small></button>
          <button type="button" data-f="cards" role="menuitem">Anki / Quizlet (.txt)<small>Front and back, ready to import</small></button>
        </div>`;
      wrap.querySelector('.xp-btn').addEventListener('click', e => { e.stopPropagation(); wrap.classList.toggle('open'); });
      document.addEventListener('click', () => wrap.classList.remove('open'));
      wrap.querySelectorAll('[data-f]').forEach(b => b.addEventListener('click', e => {
        e.stopPropagation();
        wrap.classList.remove('open');
        const d = getData();
        if (b.dataset.f === 'csv') download(`${slug(d.name)}.csv`, toCsv(d), 'text/csv');
        else download(`${slug(d.name)}-flashcards.txt`, toCards(d), 'text/plain');
      }));
      return wrap;
    },
  };
})();
