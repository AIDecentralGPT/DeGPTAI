<script lang="ts">
    import { onMount } from'svelte';

    let textContent = '';


    async function fetchTimeLineData() {
        try {
            const response = await fetch('https://usa-chat.degpt.ai/api/v0/chat/completion/proxy', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "model": "Qwen2.5-72B",
                    "messages": [
                        {
                            "role": "user",
                            "content": "1+1="
                        }
                    ],
                    "stream": true,
                    "project": "DecentralGPT",
                    "max_tokens": 50
                })
            });
            if (response.status === 200) {
                const body = response.body;
                const reader = body.getReader();
                let receivedText = "";
                const readStream = async () => {
                const { done, value } = await reader.read();
                if (!done) {
                    receivedText += new TextDecoder('utf-8').decode(value);
                    await readStream();
                } else {
                    textContent = receivedText;
                }
                };

                await readStream();
            } else {
                throw new Error('请求失败，状态码：' + response.status);
            }
            
        } catch (error) {
            console.error('Error:', error);
        }
    }

    onMount(() => {
        
    });
</script>

<main>
    <button on:click = {async() => {fetchTimeLineData()}}>开始请求</button>
    <pre>{textContent}</pre>
</main>