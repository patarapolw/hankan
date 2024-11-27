import { Dexie, type EntityTable } from "dexie";
import { type Card } from "ts-fsrs";

export interface CedictEntry {
  id?: number;
  simp: string;
  trad?: string;
  pinyin: string;
  english: string[][];
}

type SentenceId = string | number;

export interface SentenceEntry {
  id: SentenceId;
  text: string;
  trans?: string;
}

export interface SubjectEntry {
  v: string;
  sentence: {
    count: number;
    ids: SentenceId[];
  };
}

export interface UserItemEntry {
  v: string;
  srs?: Card;
  note?: string;
  skip?: boolean;
}

export default defineNuxtPlugin((nuxtApp) => {
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
    cedict: "++id, simp, [simp+trad], pinyin",
    subject: "sentence.count",
  });

  db.user.version(1).stores({
    item: "srs.difficulty, srs.due, skip",
  });

  return {
    provide: { db },
  };
});
