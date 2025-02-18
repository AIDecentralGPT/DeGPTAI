<script lang="ts">
	import { WEBUI_BASE_URL } from '$lib/constants';
	import ImagePreview from './ImagePreview.svelte';
	import { Base64 } from 'js-base64';
	import { getImageProxy } from '$lib/apis/images'

	export let src = '';
	export let alt = '';
	export let className = "";

	let _src = '';

	$: _src = src.startsWith('/') ? `${WEBUI_BASE_URL}${src}` : src;

	async function imageProxy() {
		let baseImage = await getImageProxy(Base64.encode(_src));
		if (baseImage != "") {
			_src = baseImage
		}
	}

	let showImagePreview = false;
</script>

<ImagePreview bind:show={showImagePreview} src={_src} {alt} />
<button
	on:click={() => {
		console.log('image preview');
		showImagePreview = true;
	}}
>
	<img src={_src} alt={alt} class={`max-h-64 rounded-lg ${className ? className : ''}`} draggable="false" on:error={imageProxy}/>
</button>
