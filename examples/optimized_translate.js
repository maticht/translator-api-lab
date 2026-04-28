const DEFAULT_FORMAT = "text";

export function detectSourceLanguage(text) {
  let latin = 0;
  let cyrillic = 0;

  for (const char of text) {
    const code = char.codePointAt(0);

    if (
      (code >= 0x41 && code <= 0x7a) ||
      (code >= 0x00c0 && code <= 0x024f)
    ) {
      latin += 1;
    } else if (
      (code >= 0x0400 && code <= 0x052f) ||
      (code >= 0x2de0 && code <= 0x2dff) ||
      (code >= 0xa640 && code <= 0xa69f)
    ) {
      cyrillic += 1;
    }
  }

  if (cyrillic > latin) return "ru";
  if (latin > 0) return "en";
  return null;
}

export async function translateText(baseUrl, text, target, options = {}) {
  const source =
    options.source && options.source !== "auto"
      ? options.source
      : detectSourceLanguage(text) ?? "auto";

  const payload = {
    q: text,
    source,
    target,
    format: DEFAULT_FORMAT,
  };

  const response = await fetch(`${baseUrl}/translate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Translation failed with status ${response.status}`);
  }

  return response.json();
}
