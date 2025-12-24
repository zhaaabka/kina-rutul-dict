(function () {
  const input = document.getElementById("search");
  const resultsDiv = document.getElementById("results");
  const data = window.data;

 function normalize(text) {
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0301]/g, "")
    .normalize("NFC");
}

 function normalize_q(text) {
  return text
    .replace(/[I1lӏ]/g, "Ӏ")
    .toLowerCase()
    .replace(/ˁ/g, "ˤ")
    .replace(/['’]/g, "ʼ")
    .replace(/:/g, "ː")
    .normalize("NFD")
    .replace(/[\u0301]/g, "")
    .normalize("NFC");
}

  function matchesEntry(key, entry, query) {
    const q = normalize_q(query);

    if (normalize(key).includes(q)) return true;

    for (const tr of entry.translations || []) {
      if (
        (tr.text_rus && normalize(tr.text_rus).includes(q)) ||
        (tr.text_en && normalize(tr.text_en).includes(q))
      ) {
        return true;
      }
    }

    for (const ex of entry.examples || []) {
      if (
        normalize(ex.original).includes(q) ||
        normalize(ex.translation).includes(q)
      ) {
        return true;
      }
    }

    for (const f of entry.inflection || []) {
      if (normalize(f).includes(q)) return true;
    }

    return false;
  }

  function renderEntry(key, entry) {
    const div = document.createElement("div");
    div.className = "entry";

    /* 1️⃣ Заголовок + ссылка */
    const link = `/kina-rutul-dict/words/${entry.id}.html`;

    const inflection =
      entry.inflection && entry.inflection.length
        ? `, ${entry.inflection.join(", ")}`
        : "";

    const header = `
      <a href="${link}"><b>${key}</b></a>
      (${entry.pos}${inflection})
    `;

    /* 2️⃣ Переводы */
    const translations = entry.translations
      .map(
        (t, i) =>
          `${i + 1}. ${t.text_rus || ""}${
            t.text_en ? " | " + t.text_en : ""
          };`
      )
      .join(" ");

    /* 3️⃣ Примеры */
    let examples = "";
    if (entry.examples && entry.examples.length) {
      examples =
        " Примеры: " +
        entry.examples
          .map(
            ex =>
              `<i>${ex.original}</i> — ${ex.translation};`
          )
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
        resultsDiv.appendChild(renderEntry(key, entry));
      }
    }
  });
})();

// ===== virtual keyboard =====
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

    // запускаем поиск
    input.dispatchEvent(new Event("input"));

    input.focus();
  });
});
