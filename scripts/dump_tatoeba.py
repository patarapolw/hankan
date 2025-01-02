from wordfreq import zipf_frequency
from regex import Regex
import jieba

import sqlite3
from urllib.request import urlretrieve
import tarfile
import bz2
import json
from pathlib import Path

tmp_root = Path('tmp')
tmp_root.mkdir(exist_ok=True)


def dump_tatoeba(lang: str):
    db = sqlite3.connect(f"public/tatoeba_{lang}.db")

    db.executescript(
        f"""
        CREATE TABLE IF NOT EXISTS tatoeba (
            id      INT NOT NULL PRIMARY KEY,
            txt     TEXT NOT NULL,
            eng     TEXT,
            voc     JSON,
            f       FLOAT
        );

        CREATE INDEX IF NOT EXISTS idx_tatoeba_f ON tatoeba (f);
        """
    )

    if not db.execute("SELECT 1 FROM tatoeba LIMIT 1").fetchall():
        _download_tatoeba(lang)
        _download_tatoeba("eng")

        _download_tatoeba_links()

        print("Building sentence dictionary...")

        db.executescript(
            f"""
            CREATE UNIQUE INDEX idx_u_{lang} ON tatoeba (txt);

            CREATE TEMP TABLE eng (
                id      INT NOT NULL PRIMARY KEY,
                eng     TEXT NOT NULL
            );

            CREATE TEMP TABLE links (
                id1     INT,
                id2     INT,
                PRIMARY KEY (id1, id2)
            );
            """
        )

        cmn_ids = set()
        eng_ids = set()

        for ln in (tmp_root / f"{lang}_sentences.tsv").open("r", encoding="utf8"):
            rs = ln.rstrip().split("\t", 1)
            cmn_ids.add(int(rs[0]))

        for ln in (tmp_root / "eng_sentences.tsv").open("r", encoding="utf8"):
            rs = ln.rstrip().split("\t", 1)
            eng_ids.add(int(rs[0]))

        for ln in (tmp_root / "links.csv").open("r", encoding="utf8"):
            rs = ln.split("\t", 2)

            id1 = int(rs[0])
            id2 = int(rs[1])

            if id1 in cmn_ids and id2 in eng_ids:
                db.execute("INSERT INTO links (id1,id2) VALUES (?,?)", (id1, id2))

        db.commit()

        for ln in (tmp_root / "eng_sentences.tsv").open("r", encoding="utf8"):
            rs = ln.rstrip().split("\t")
            db.execute("INSERT INTO eng (id, eng) VALUES (?,?)", (int(rs[0]), rs[2]))

        db.commit()

        re_en = Regex(r"[A-Za-z]")
        re_han = Regex(r"^[\p{Han}\p{Katakana}\p{Hiragana}ー・＝]+$")

        for ln in (tmp_root / f"{lang}_sentences.tsv").open("r", encoding="utf8"):
            rs = ln.rstrip().split("\t")

            id1 = rs[0]
            sentence = rs[2]

            if re_en.search(sentence):
                continue

            f = 0
            voc = set()
            vs = jieba.cut_for_search(sentence)
            for v in vs:
                if re_han.fullmatch(v):
                    if v not in voc:
                        voc.add(v)
                        f += zipf_frequency(v, lang)

            db.execute(
                """
                INSERT INTO tatoeba (id, txt, eng, voc, f) VALUES (?,?,(
                    SELECT eng FROM eng WHERE id = (
                        SELECT id2 FROM links WHERE id1 = ?
                    )
                ),?,?)
                ON CONFLICT DO NOTHING
                """,
                (
                    id1,
                    sentence,
                    id1,
                    json.dumps(list(voc), ensure_ascii=False),
                    f,
                ),
            )

        db.commit()

        db.executescript(
            f"""
            DROP TABLE eng;
            DROP TABLE links;
            DROP INDEX idx_u_{lang};
            """
        )

        print("Done")


def _download_tatoeba(lang: str):
    filename = f"{lang}_sentences.tsv"

    if not (tmp_root / filename).exists():
        zipFilename = f"{lang}_sentences.tsv.bz2"
        zipPath = tmp_root / zipFilename

        url = f"https://downloads.tatoeba.org/exports/per_language/{lang}/{zipFilename}"
        print("Downloading {} from {}".format(filename, url))
        urlretrieve(url, zipPath)

        with (tmp_root / filename).open("wb") as unzipFile:
            with bz2.open(zipPath) as zipFile:
                unzipFile.write(zipFile.read())


def _download_tatoeba_links():
    filename = "links.csv"

    if not (tmp_root / filename).exists():
        zipFilename = "links.tar.bz2"
        zipPath = tmp_root / zipFilename

        url = f"https://downloads.tatoeba.org/exports/{zipFilename}"
        print("Downloading {} from {}".format(filename, url))
        urlretrieve(url, zipPath)

        with tarfile.open(zipPath) as z:
            z.extract(filename, tmp_root)


if __name__ == "__main__":
    dump_tatoeba('cmn')
