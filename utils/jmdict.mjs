//@ts-check

import { ofetch } from "ofetch";

/**
 *
 * @returns {Promise<{jmdict: string; jmnedict: string; kanjidic2: string}>}
 */
export async function getJMDictLinks() {
  const ghAPI = "https://api.github.com/repos/scriptin/jmdict-simplified";

  const out = {};

  const r = await ofetch(ghAPI + "/releases/latest");
  for (const a of r.assets) {
    if (/^jmdict-examples-eng-\d.+\.zip$/.test(a.name)) {
      out.jmdict = a.browser_download_url;
      continue;
    }

    if (/^jmnedict-all-\d.+\.zip$/.test(a.name)) {
      out.jmnedict = a.browser_download_url;
      continue;
    }

    if (/^kanjidic2-en-\d.+\.zip$/.test(a.name)) {
      out.kanjidic2 = a.browser_download_url;
      continue;
    }
  }

  return out;
}
