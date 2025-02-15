<script>
    import { onMount } from'svelte';
    // 接收推文 ID 和主题作为属性
    export let tweetId;
    export let theme;
    export let isTwitterScriptLoaded = false;
    let tweetContainer;

    const createTweetWithTheme = () => {
        tweetContainer.innerHTML = '';
        twttr.widgets.createTweet(
            tweetId,
            tweetContainer,
            {
                theme: theme
            }
        );
    };

    onMount(() => {
        if (isTwitterScriptLoaded) {
            createTweetWithTheme();
        }
    });

    // 当主题属性改变时重新创建推文
    $: if (isTwitterScriptLoaded && tweetContainer) {
        createTweetWithTheme();
    }

    $: if (theme) {
        if (isTwitterScriptLoaded && tweetContainer) {
            createTweetWithTheme();
        }
    }
</script>

<div class="w-[320px]" bind:this={tweetContainer} />