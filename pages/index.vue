<template>
  <div></div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();

console.log("Public runtime config:", config.public);
navigateTo(`/${config.public.lang}`);
</script>

<style lang="scss" scoped></style>
