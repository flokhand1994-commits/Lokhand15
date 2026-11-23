// Soft female text-to-speech, shared by all flashcard and word-list pages.
// Browsers only offer the voices installed on the device, so we score them:
// known female voices and natural-sounding ones win, known male voices lose.
(function () {
  const FEMALE = /female|woman|ellen|claire|fenna|colette|dena|amélie|amelie|audrey|aurélie|aurelie|marie|julie|hortense|denise|eloise|vivienne|céline|celine|charline|mónica|monica|paulina|marisol|helena|laura|elvira|ximena|alice|federica|elsa|isabella|milena|katya|irina|svetlana|dariya|tingting|ting-ting|meijia|sinji|huihui|xiaoxiao|xiaoyi|yaoyao|kyoko|o-ren|haruka|ayumi|nanami|yuna|sora|heami|sunhi|jimin/i;
  const MALE = /\bmale\b|xander|thomas|henri|arnaud|maarten|frank|luca|diego|jorge|pablo|alvaro|cosimo|pavel|dmitry|yuri|kangkang|yunxi|yunyang|ichiro|keita|otoya|hattori|injoon|minsu|daniel|rocko|grandpa|reed|eddy/i;
  let voices = [];
  let current = null;            // keep a reference: Chrome can cut off utterances that get garbage-collected
  const cache = {};

  function load() {
    voices = window.speechSynthesis ? speechSynthesis.getVoices() : [];
    for (const k in cache) delete cache[k];
  }

  function pick(lang) {
    if (cache[lang] !== undefined) return cache[lang];
    const base = lang.split('-')[0].toLowerCase();
    let best = null, bestScore = -Infinity;
    for (const v of voices) {
      const vl = (v.lang || '').replace('_', '-').toLowerCase();
      if (!vl.startsWith(base)) continue;
      let score = 0;
      if (vl === lang.toLowerCase()) score += 1;
      if (FEMALE.test(v.name)) score += 4;
      if (MALE.test(v.name)) score -= 6;
      if (/natural|neural|online|premium|enhanced|siri/i.test(v.name)) score += 2;
      if (/^google/i.test(v.name)) score += 2;          // Google's voices are female by default
      if (v.localService) score += 0.5;
      if (score > bestScore) { best = v; bestScore = score; }
    }
    return voices.length ? (cache[lang] = best) : best;
  }

  // First choice: Google's text-to-speech — a natural female voice with correct
  // pronunciation on every device. Device voices vary a lot (a phone without a Dutch
  // voice reads Dutch with an English one), so they are only the fallback.
  // Google refuses audio requests that carry a Referer header, and audio elements
  // can't drop it themselves — so the page stops sending referrers.
  const meta = document.createElement('meta');
  meta.name = 'referrer';
  meta.content = 'no-referrer';
  document.head.appendChild(meta);

  let audio = null;
  window.softSpeak = function (text, lang) {
    if (!text) return;
    if (audio) audio.pause();
    if (window.speechSynthesis) speechSynthesis.cancel();
    const tl = lang.toLowerCase().startsWith('zh') ? 'zh-CN' : lang.split('-')[0];
    audio = new Audio();
    audio.preservesPitch = true;
    audio.defaultPlaybackRate = audio.playbackRate = 0.9;
    audio.volume = 0.9;
    let fellBack = false;
    const fallback = () => { if (!fellBack) { fellBack = true; deviceSpeak(text, lang); } };
    audio.onerror = fallback;
    audio.src = `https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=${tl}&q=${encodeURIComponent(String(text).slice(0, 200))}`;
    audio.play().catch(e => { if (e.name !== 'AbortError') fallback(); });   // AbortError = the next tap replaced it
  };

  function deviceSpeak(text, lang) {
    if (!window.speechSynthesis) return;
    if (!voices.length) load();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = lang;
    const v = pick(lang);
    if (v) u.voice = v;
    u.rate = 0.9;       // a little slower and calmer; pitch stays natural
    u.volume = 0.9;
    current = u;
    if (speechSynthesis.speaking || speechSynthesis.pending) {
      speechSynthesis.cancel();
      setTimeout(() => speechSynthesis.speak(u), 80);   // Chrome can drop a speak() right after cancel()
    } else {
      speechSynthesis.speak(u);
    }
  };

  // A listen button for pages without their own handler:
  // <button class="say" data-say="text" data-say-lang="nl-BE">🔊</button>
  window.speakButton = function (text, lang) {
    const t = String(text).replace(/<[^>]*>/g, '').replace(/"/g, '&quot;');
    return `<button type="button" class="say" data-say="${t}" data-say-lang="${lang}" aria-label="Listen">🔊</button>`;
  };
  document.addEventListener('click', e => {
    const b = e.target.closest && e.target.closest('[data-say-lang]');
    if (!b) return;
    e.stopPropagation();          // don't flip the card underneath
    e.preventDefault();
    softSpeak(b.dataset.say, b.dataset.sayLang);
  }, true);
  const style = document.createElement('style');
  style.textContent = '.say{border:none;background:none;font-size:.95em;cursor:pointer;opacity:.75;padding:0 4px;vertical-align:middle}.say:hover{opacity:1}';
  document.head.appendChild(style);

  if (window.speechSynthesis) {
    load();
    speechSynthesis.addEventListener('voiceschanged', load);
  }
})();
