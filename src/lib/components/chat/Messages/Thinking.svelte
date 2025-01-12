<script lang="ts">
	import { getContext } from 'svelte';
	const i18n = getContext('i18n');
</script>

<span class="text-animation text-sm font-bold">
	{ $i18n.t("Thinking...") }
</span>
<style>
	.text-animation {
      display: inline-block;
      background: linear-gradient(90deg, #333, #999 25%, #333 50%, #999 75%, #333);
      background-size: 200%;
      background-clip: text;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: animate-gradient 1.5s linear infinite;
    }
	@keyframes animate-gradient {
    0% {
			background-position: 200% 0;
    }
    100% {
      background-position: 0 0;
    }
  }
</style>
