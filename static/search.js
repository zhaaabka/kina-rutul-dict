(function () {
  const input = document.getElementById("search");
  const resultsDiv = document.getElementById("results");
  const data = window.data;

 function normalize(text) {
  return text
    .replace(/[I1ӏ]/g, "Ӏ")
    .toLowerCase()
    .replace(/ˁ/g, "ˤ")
    .replace(/['’]/g, "ʼ")
    .replace(/:/g, "ː")
    .normalize("NFD")
    .replace(/[\u0301]/g, "")
    .normalize("NFC");
}

function getSearchMode() {
  const btn = document.getElementById("search-mode-btn");
  return btn ? btn.dataset.mode : "all";
}


 function matchesEntry(key, entry, query) {
  const q = normalize(query);
  const mode = getSearchMode();

  function match(text) {
    return text && normalize(text).includes(q);
  }

 
    if (mode === "lemma" || mode === "all") {
        if (match(key)) return true;

        for (const f of entry.inflection || []) {
        if (match(f)) return true;
  }
}

  
  if (mode === "translation" || mode === "all") {
    for (const tr of entry.translations || []) {
      if (match(tr.text_rus) || match(tr.text_en)) {
        return true;
      }
    }
  }

 
  if (mode === "example" || mode === "all") {
    for (const ex of entry.examples || []) {
      if (match(ex.original)) return true;
    }
  }

  
  if (mode === "example_translation" || mode === "all") {
    for (const ex of entry.examples || []) {
      if (match(ex.translation)) return true;
    }
  }

  return false;
}

  function highlight(text, query) {
  if (!query) return text;

  const normText = normalize(text);
  const normQuery = normalize(query);

  if (!normQuery) return text;

  let result = "";
  let i = 0;

  while (i < text.length) {
    if (normText.slice(i, i + normQuery.length) === normQuery) {
      result += `<mark>${text.slice(i, i + normQuery.length)}</mark>`;
      i += normQuery.length;
    } else {
      result += text[i];
      i++;
    }
  }

  return result;
}

  function renderEntry(key, entry, query) {
    const mode = getSearchMode();
    const div = document.createElement("div");
    div.className = "entry";


    const link = `/kina-rutul-dict/words/${entry.id}.html`;

    const inflection =
        entry.inflection && entry.inflection.length
            ? `, ${entry.inflection
                .map(f =>
                    (mode === "lemma" || mode === "all")
                    ? highlight(f, query)
                    : f
                )
                .join(", ")}`
            : "";


    const header = `
        <a href="${link}">
            <b>${
                (mode === "lemma" || mode === "all")
                ? highlight(key, query)
                : key
            }</b>
        </a>
        (${entry.pos}${inflection})
    `;


    const translations = entry.translations
        .map((t, i) => {
            const rus =
            (mode === "translation" || mode === "all")
                ? highlight(t.text_rus, query)
                : t.text_rus;

            const eng =
            (mode === "translation" || mode === "all")
                ? highlight(t.text_en, query)
                : t.text_en;

            return `${i + 1}. ${rus || ""}${eng ? " | " + eng : ""};`;
        })
        .join(" ");


 
    let examples = "";
    if (entry.examples && entry.examples.length) {
    examples =
        " Примеры: " +
        entry.examples
        .map(ex => {
            const original =
            (mode === "example" || mode === "all")
                ? highlight(ex.original, query)
                : ex.original;

            const translation =
            (mode === "example_translation" || mode === "all")
                ? highlight(ex.translation, query)
                : ex.translation;

            return `<i>${original}</i> — ${translation};`;
        })
        .join(" ");
}


    div.innerHTML = `
      ${header}: ${translations}${examples}
    `;

    return div;
  }

  input.addEventListener("input", () => {
    const query = input.value.trim();
    resultsDiv.innerHTML = "";

    if (query.length < 2) return;

    for (const [key, entry] of Object.entries(data)) {
      if (matchesEntry(key, entry, query)) {
        resultsDiv.appendChild(renderEntry(key, entry, query));
      }
    }
  });
})();


document.querySelectorAll(".virtual-key").forEach(key => {
  key.addEventListener("click", () => {
    const input = document.getElementById("search");

    const start = input.selectionStart;
    const end = input.selectionEnd;

    const char = key.textContent;

    input.value =
      input.value.slice(0, start) +
      char +
      input.value.slice(end);

    input.selectionStart = input.selectionEnd = start + char.length;

    
    input.dispatchEvent(new Event("input"));

    input.focus();
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('search-mode-btn');
  const input = document.getElementById('search');

  const placeholders = {
    all: 'Search anywhere in the entry',
    lemma: 'Search lemma or word forms',
    translation: 'Search Russian or English translations',
    example: 'Search example sentences',
    example_translation: 'Search translations of examples'
  };

  document.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', e => {
      e.preventDefault();

      const mode = item.dataset.mode;
      const text = item.textContent;

      // обновляем кнопку
      btn.textContent = text;
      btn.dataset.mode = mode;

      // активный пункт
      document.querySelectorAll('.dropdown-item')
        .forEach(i => i.classList.remove('active'));
      item.classList.add('active');

      // placeholder
      input.placeholder = placeholders[mode] || 'Search';

      // фокус обратно в поле
      input.focus();
    });
  });

  // начальный placeholder
  input.placeholder = placeholders[btn.dataset.mode] || 'Search';
});

