//@ts-check

import { writeFile } from "fs/promises";
import { Blob } from "buffer";
import { ofetch } from "ofetch";
import { BlobReader, ZipReader, TextWriter } from "@zip.js/zip.js";
import { getJMDictLinks } from "../utils/jmdict.mjs";

const r = await getJMDictLinks();

await extract("jmdict");
await extract("jmnedict");
await extract("kanjidic2");

/**
 *
 * @param {keyof typeof r} name
 */
async function extract(name) {
  const buffer = Buffer.from(
    await ofetch(r[name], { responseType: "arrayBuffer" }),
  );
  const blob = new Blob([buffer]);

  await writeFile(`public/${name}.zip`, buffer);

  const bReader = new BlobReader(blob);
  const reader = new ZipReader(bReader);
  const writer = new TextWriter();

  const entries = await reader.getEntries();
  if (!entries[0].getData) {
    throw entries;
  }

  await writeFile(`tmp/${name}.json`, await entries[0].getData(writer));
}
