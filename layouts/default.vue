<template>
  <v-app>
    <v-layout>
      <v-navigation-drawer expand-on-hover rail :mobile="false">
        <v-list>
          <v-list-item title="Home">
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
          <v-list-item prepend-icon="mdi-text-recognition" title="Text"></v-list-item>
          <v-list-item prepend-icon="mdi-information-outline" title="About"></v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-container>
        <slot />
      </v-container>
    </v-layout>
  </v-app>
</template>

<script setup lang="ts">
const level = ref(0);
</script>
