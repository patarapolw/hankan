from wordfreq import zipf_frequency
from regex import Regex

import sqlite3


def dump_wordfreq_zh():
    db = sqlite3.connect("public/cedict.db")
    re_han = Regex(r"^\p{Han}+$")

    db.executescript(
        f"""
        CREATE TABLE IF NOT EXISTS wordfreq (
            v   TEXT NOT NULL PRIMARY KEY,
            f   FLOAT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_wordfreq_f ON wordfreq (f);
        """
    )


    for r in db.execute("SELECT DISTINCT v FROM (SELECT simp v FROM cedict UNION SELECT trad v FROM cedict)"):
        v = r[0]
        if not v or not re_han.fullmatch(v):
            continue

        db.execute(
            "INSERT INTO wordfreq (v, f) VALUES (?,?) ON CONFLICT DO NOTHING",
            (v, zipf_frequency(v, "zh")),
        )

    db.commit()

    print("Done")


if __name__ == "__main__":
    dump_wordfreq_zh()
