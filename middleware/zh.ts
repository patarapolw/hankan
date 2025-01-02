import { BlobReader, ZipReader, TextWriter } from "@zip.js/zip.js";
import { type CedictEntry } from "~/plugins/db";

export default defineNuxtRouteMiddleware(async (to, from) => {
  const { $db } = useNuxtApp();

  const nCedict = await $db.dict.cedict.count();

  if (nCedict) {
  } else {
    try {
      const data = await $fetch<Blob>(
        "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip",
        { responseType: "blob" },
      );

      const bReader = new BlobReader(data);
      const reader = new ZipReader(bReader);
      const writer = new TextWriter();

      const entries = await reader.getEntries();
      const txt = await entries[0].getData!(writer);

      const rs: CedictEntry[] = [];

      for (const ln of txt.split("\n")) {
        if (ln[0] === "#") continue;

        const m = /^(\p{sc=Han}+) (\p{sc=Han}+) \[(.+?)\] \/(.+)\//u.exec(ln);
        if (!m) continue;

        const r: CedictEntry = {
          simp: m[2],
          pinyin: m[3],
          english: m[4].split("/").map((s) => s.split(";")),
        };

        if (m[1] !== m[2]) {
          r.trad = m[1];
        }

        rs.push(r);
      }

      if (rs.length) {
        await $db.dict.cedict.bulkAdd(rs);
      } else {
        throw { txt: txt.substring(0, 100), rs };
      }
    } catch (e) {
      console.error(e);
      return;
    }
  }
});
