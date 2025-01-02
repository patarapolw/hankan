//@ts-check

import { BlobReader, ZipReader, TextWriter } from "@zip.js/zip.js";
import { ofetch } from "ofetch";

export async function downloadCedict() {
  const data = await ofetch(
    "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip",
    { responseType: "blob" },
  );

  const bReader = new BlobReader(data);
  const reader = new ZipReader(bReader);
  const writer = new TextWriter();

  const entries = await reader.getEntries();
  if (!entries[0].getData) {
    throw entries;
  }

  const txt = await entries[0].getData(writer);

  /** @type {import('~/plugins/db').CedictEntry[]} */
  const rs = [];

  for (const ln of txt.split("\n")) {
    if (ln[0] === "#") continue;

    const m = /^(\p{sc=Han}+) (\p{sc=Han}+) \[(.+?)\] \/(.+)\//u.exec(ln);
    if (!m) continue;

    const r = {
      simp: m[2],
      trad: "",
      pinyin: m[3],
      english: m[4].split("/").map((s) => s.split(";")),
    };

    if (m[1] !== m[2]) {
      r.trad = m[1];
    } else {
      // @ts-ignore
      delete r.trad;
    }

    rs.push(r);
  }

  if (rs.length) {
    return rs;
  }
  throw { txt: txt.substring(0, 100), rs };
}
