(function () {
  const input = document.getElementById("search");
  const resultsDiv = document.getElementById("results");

  const entries = window.data;

  function normalize(text) {
    return text
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036fːʼʁɨ]/g, "");
  }

  function entryMatches(entry, query) {
    const q = normalize(query);

    if (normalize(entry.lemma).includes(q)) return true;

    if (entry.translations) {
      for (const tr of entry.translations) {
        if (normalize(tr.text).includes(q)) return true;
      }
    }

    if (entry.examples) {
      for (const ex of entry.examples) {
        if (
          normalize(ex.original).includes(q) ||
          normalize(ex.translation).includes(q)
        ) {
          return true;
        }
      }
    }

    return false;
  }

  function renderEntry(entry) {
    const div = document.createElement("div");
    div.className = "entry";

    div.innerHTML = `
      <div class="lemma">${entry.lemma}</div>
      ${entry.pos ? `<div class="pos">${entry.pos}</div>` : ""}

      ${entry.translations?.map(t =>
        `<div>• ${t.text}</div>`
      ).join("") || ""}

      ${entry.examples?.map(ex =>
        `<div class="example">"${ex.original}" — ${ex.translation}</div>`
      ).join("") || ""}
    `;

    return div;
  }

  input.addEventListener("input", () => {
    const query = input.value.trim();
    resultsDiv.innerHTML = "";

    if (query.length < 2) return;

    Object.values(entries).forEach(entry => {
      if (entryMatches(entry, query)) {
        resultsDiv.appendChild(renderEntry(entry));
      }
    });
  });
})();
