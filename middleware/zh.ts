import { downloadCedict } from "~/utils/cedict.mjs";

export default defineNuxtRouteMiddleware(async (to, from) => {
  const { $db } = useNuxtApp();

  const nCedict = await $db.dict.cedict.count();

  if (nCedict) {
  } else {
    try {
      $db.dict.cedict.bulkAdd(await downloadCedict());
    } catch (e) {
      console.error(e);
      return;
    }
  }
});
