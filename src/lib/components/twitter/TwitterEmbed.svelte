<script>
    import { onMount } from'svelte';
    // 接收推文 ID 和主题作为属性
    export let tweetId;
    export let theme;
    let tweetContainer;
    let isTwitterScriptLoaded = false;

    const loadTwitterScript = () => {
        if (isTwitterScriptLoaded) return;
        const script = document.createElement('script');
        script.src = 'https://platform.twitter.com/widgets.js';
        script.charset = 'utf-8';
        script.async = true;
        script.onload = () => {
            isTwitterScriptLoaded = true;
            if (typeof twttr!== 'undefined' && tweetContainer) {
                createTweetWithTheme();
            }
        };
        document.head.appendChild(script);
    };

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
        loadTwitterScript();
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

<div bind:this={tweetContainer} />