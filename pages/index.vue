<template>
  <div>
    <v-sheet class="d-flex justify-center">
      <v-btn class="text-none text-subtitle-1" color="secondary" rounded="lg">
        <span class="item">Start Quiz</span>
        <span class="item d-flex-text" v-if="nRemaining + nNew > 0">
          {{ "(" }}
          <span>{{ nRemaining }}</span>
          <small v-if="nNew">+{{ nNew }}</small>
          {{ ")" }}
        </span>
      </v-btn>
    </v-sheet>
    <v-sheet class="d-flex-text justify-center mt-3">
      <span class="item" lang="zh-CN">汉字:</span>
      <span class="item">{{ nHan }}</span>
      <span class="item">{{ "," }}</span>
      <span class="item" lang="zh-CN">生词:</span>
      <span class="item">{{ nVoc }} </span>
      <span class="item">{{ `(${Math.round(percentCorrect * 100)}%)` }}</span>
    </v-sheet>
    <v-sheet>
      <v-menu v-for="(c, i) in allHan" :key="i">
        <template v-slot:activator="{ props }">
          <v-avatar v-bind="props" color="info">
            {{ c }}
          </v-avatar>
        </template>
        <v-list>
          <v-list-item>
            <span class="text-h1">
              {{ c }}
            </span>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item style="text-align: center">Open</v-list-item>
        </v-list>
      </v-menu>
    </v-sheet>
  </div>
</template>

<script setup lang="ts">
const nRemaining = ref(46);
const nNew = ref(1);

const nHan = ref(402);
const nVoc = ref(1166);
const percentCorrect = ref(0.48);

const allHan = ref("アイウエアブランド");
</script>

<style lang="scss" scoped>
.d-flex-text {
  display: flex;
  flex-direction: row;
  align-items: end;
}

.item + .item {
  margin-left: 0.3em;
}
</style>
