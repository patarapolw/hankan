<template>
  <v-app>
    <v-layout>
      <v-navigation-drawer expand-on-hover rail :mobile="false">
        <v-list>
          <v-list-item title="Home" to="/">
            <template v-slot:prepend>
              <v-avatar color="info">
                <v-icon icon="mdi-home" size="x-small"></v-icon>
              </v-avatar>
            </template>
          </v-list-item>
        </v-list>
        <v-divider></v-divider>
        <v-list nav density="compact">
          <v-list-item prepend-icon="mdi-plus" title="Add"></v-list-item>
          <v-list-item prepend-icon="mdi-minus" title="Skip"></v-list-item>
          <v-list-item prepend-icon="mdi-magnify" title="Search"></v-list-item>
          <v-list-item title="Levels" @click="level = level ? 0 : 3">
            <template v-slot:prepend>
              <v-avatar v-if="level" color="surface-light">
                <span class="text">{{ level }}</span>
              </v-avatar>
              <v-icon v-else icon="mdi-numeric"></v-icon>
            </template>
          </v-list-item>
          <v-list-item
            prepend-icon="mdi-text-recognition"
            title="Text"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-information-outline"
            title="About"
          ></v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-container>
        <slot />
      </v-container>
    </v-layout>
    <v-dialog
      :model-value="loadingMessage !== null"
      persistent
      :max-width="800"
    >
      <v-card>
        <v-card-text>
          <p v-for="(ln, i) in loadingMessage" :key="i">
            {{ ln }}
          </p>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script setup lang="ts">
// import { BlobReader, ZipReader, TextWriter } from "@zip.js/zip.js";
// import { type CedictEntry } from "~/plugins/db";

// const { $db } = useNuxtApp();

const level = ref(0);
const loadingMessage = ref<string[] | null>([]);

// useAsyncData(async () => {
//   const nCedict = await $db.dict.cedict.count();

//   if (nCedict) {
//     loadingMessage.value = null;
//   } else {
//     const msgs = [];
//     msgs.push("Downlading CC-CEDICT...");
//     loadingMessage.value = Array.from(msgs);
//     try {
//       const data = await $fetch<Blob>(
//         "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip",
//         { responseType: "blob" },
//       );

//       const bReader = new BlobReader(data);
//       const reader = new ZipReader(bReader);
//       const writer = new TextWriter();

//       const entries = await reader.getEntries();
//       const txt = await entries[0].getData!(writer);

//       const rs: CedictEntry[] = [];

//       for (const ln of txt.split("\n")) {
//         if (ln[0] === "#") continue;

//         const m = /^(\p{sc=Han}+) (\p{sc=Han}+) \[(.+?)\] \/(.+)\//u.exec(ln);
//         if (!m) continue;

//         const r: CedictEntry = {
//           simp: m[2],
//           pinyin: m[3],
//           english: m[4].split("/").map((s) => s.split(";")),
//         };

//         if (m[1] !== m[2]) {
//           r.trad = m[1];
//         }

//         rs.push(r);
//       }

//       if (rs.length) {
//         await $db.dict.cedict.bulkAdd(rs);
//       } else {
//         throw { txt: txt.substring(0, 100), rs };
//       }
//     } catch (e) {
//       console.error(e);
//       msgs.push("Fail to download CC-CEDICT. Please supply the dictionary.");
//       loadingMessage.value = Array.from(msgs);

//       return;
//     }

//     loadingMessage.value = null;
//   }
// });
</script>
