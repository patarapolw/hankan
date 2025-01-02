//@ts-check

import { writeFileSync } from "fs";
import initSqlJs from "sql.js";
import { downloadCedict } from "../utils/cedict.mjs";

const SQL = await initSqlJs();
const db = new SQL.Database();
db.run(/* sql */ `
    CREATE TABLE IF NOT EXISTS cedict (
        simp    TEXT NOT NULL,
        trad    TEXT,
        pinyin  TEXT NOT NULL,
        english JSON NOT NULL,
        [data]  JSON
    );

    CREATE INDEX IF NOT EXISTS idx_cedict_simp ON cedict (simp);
    CREATE INDEX IF NOT EXISTS idx_cedict_trad ON cedict (trad);
`);

const rs = await downloadCedict();

while (rs.length) {
  const ss = rs.splice(0, 1000);
  db.run(
    /* sql */ `INSERT INTO cedict (simp, trad, pinyin, english) VALUES ` +
      ss.map((_) => "(?,?,?,?)").join(","),
    ss.flatMap((s) => [
      s.simp,
      s.trad || null,
      s.pinyin,
      JSON.stringify(s.english),
    ]),
  );
}

writeFileSync("public/cedict.db", Buffer.from(db.export()));
