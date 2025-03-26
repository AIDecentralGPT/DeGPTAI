<script lang="ts">
	import { createEventDispatcher } from'svelte';
	import { WEBUI_BASE_URL } from '$lib/constants';
	import ImagePreview from './ImagePreview.svelte';
	import { Base64 } from 'js-base64';
	import { getImageProxy } from '$lib/apis/images'

	export let src = '';
	export let alt = '';
	export let className = "";
	export let imgIndex = 0;

	const dispatch = createEventDispatcher();

	let _src = '';

	$: _src = src.startsWith('/') ? `${WEBUI_BASE_URL}${src}` : src;

	function imageProxy() {
		getImageProxy(Base64.encode(_src)).then(result => {
			if (result.data != "") {
				_src = result.data
			}
		});
		_src = "/static/picture_loading.png"
	}

	function handleImageError() {
    dispatch('imageLoadFailed', { index: imgIndex });
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
	<img src={_src} alt={alt} class={`max-h-64 rounded-lg ${className ? className : ''}`} draggable="false" on:error={handleImageError}/>
</button>
