<script lang="ts">
<<<<<<< HEAD
=======
	import { createEventDispatcher } from'svelte';
>>>>>>> fingerprintAuth-out
	import { WEBUI_BASE_URL } from '$lib/constants';
	import ImagePreview from './ImagePreview.svelte';
	import { Base64 } from 'js-base64';
	import { getImageProxy } from '$lib/apis/images'

	export let src = '';
	export let alt = '';
	export let className = "";
<<<<<<< HEAD
=======
	export let imgIndex = 0;

	const dispatch = createEventDispatcher();
>>>>>>> fingerprintAuth-out

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

<<<<<<< HEAD
=======
	function handleImageError() {
    dispatch('imageLoadFailed', { index: imgIndex });
  }

>>>>>>> fingerprintAuth-out
	let showImagePreview = false;
</script>

<ImagePreview bind:show={showImagePreview} src={_src} {alt} />
<<<<<<< HEAD
<button
=======
<button 
>>>>>>> fingerprintAuth-out
	on:click={() => {
		console.log('image preview');
		showImagePreview = true;
	}}
>
<<<<<<< HEAD
	<img src={_src} alt={alt} class={`max-h-64 rounded-lg ${className ? className : ''}`} draggable="false" on:error={imageProxy}/>
=======
	<img src={_src} alt={alt} class={`max-h-64 rounded-lg ${className ? className : ''}`} draggable="false" on:error={handleImageError}/>
>>>>>>> fingerprintAuth-out
</button>
