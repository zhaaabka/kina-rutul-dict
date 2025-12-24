(function () {
  const input = document.getElementById("search");
  const resultsDiv = document.getElementById("results");

  const data = window.data;

  function normalize(text) {
    return text
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036fːʼʁɨˤʷ]/g, "");
  }

  function matchesEntry(key, entry, query) {
    const q = normalize(query);

    // 1. Заголовок (ключ словаря)
    if (normalize(key).includes(q)) return true;

    // 2. Переводы
    for (const tr of entry.translations || []) {
      if (
        (tr.text_rus && normalize(tr.text_rus).includes(q)) ||
        (tr.text_en && normalize(tr.text_en).includes(q))
      ) {
        return true;
      }
    }

    // 3. Примеры
    for (const ex of entry.examples || []) {
      if (
        normalize(ex.original).includes(q) ||
        normalize(ex.translation).includes(q)
      ) {
        return true;
      }
    }

    // 4. Словоизменение
    for (const form of entry.inflection || []) {
      if (normalize(form).includes(q)) return true;
    }

    return false;
  }

  function renderEntry(key, entry) {
    const div = document.createElement("div");
    div.className = "entry";

    const translations = entry.translations
      .map(t => `• ${t.text_rus}${t.text_en ? " — " + t.text_en : ""}`)
      .join("<br>");

    const examples = (entry.examples || [])
      .map(ex =>
        `<div class="example">"${ex.original}" — ${ex.translation}</div>`
      )
      .join("");

    const inflection = entry.inflection.length
      ? `<div><b>Формы:</b> ${entry.inflection.join(", ")}</div>`
      : "";

    div.innerHTML = `
      <div class="lemma">${key}</div>
      <div class="pos">${entry.pos}</div>
      <div>${translations}</div>
      ${inflection}
      ${examples}
    `;

    return div;
  }

  input.addEventListener("input", () => {
    const query = input.value.trim();
    resultsDiv.innerHTML = "";

    if (query.length < 2) return;

    for (const [key, entry] of Object.entries(data)) {
      if (matchesEntry(key, entry, query)) {
        resultsDiv.appendChild(renderEntry(key, entry));
      }
    }
  });
})();
