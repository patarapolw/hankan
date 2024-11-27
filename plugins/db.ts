import { Dexie, type EntityTable } from "dexie";

export interface CedictEntry {
  id: number;
  simp: string;
  trad?: string;
  pinyin: string[];
  english: string[][];
}

type SentenceId = string | number;

export interface SentenceEntry {
  id: SentenceId;
  text: string;
  lang: "cmn" | "eng";
  trans?: SentenceId;
}

export interface SubjectEntry {
  v: string;
  freq: {
    cmn: string;
  };
  sentence: {
    count: number;
    ids: SentenceId[];
  };
}

export interface UserItemEntry {
  v: string;
  srs: {};
  note?: string;
}

export default defineNuxtPlugin(async (nuxtApp) => {
  const db = {
    dict: new Dexie("dict") as Dexie & {
      cedict: EntityTable<CedictEntry, "id">;
      sentence: EntityTable<SentenceEntry, "id">;
      subject: EntityTable<SubjectEntry, "v">;
    },
    user: new Dexie("user") as Dexie & {
      item: EntityTable<UserItemEntry, "v">;
    },
  };

  db.dict.version(1).stores({
    cedict: "++id, simp, [simp+trad], *pinyin",
  });

  return {
    provide: { db },
  };
});
