<template>
  <v-app>
    <v-layout>
      <v-navigation-drawer expand-on-hover rail>
        <v-list>
          <v-list-item prepend-icon="mdi-account-circle" title="Account"></v-list-item>
        </v-list>
        <v-divider></v-divider>
        <v-list nav density="compact">
          <v-list-item prepend-icon="mdi-plus" title="Add"></v-list-item>
          <v-list-item prepend-icon="mdi-minus" title="Skip"></v-list-item>
          <v-list-item prepend-icon="mdi-magnify" title="View"></v-list-item>
          <v-list-item prepend-icon="mdi-numeric" title="Levels"></v-list-item>
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
