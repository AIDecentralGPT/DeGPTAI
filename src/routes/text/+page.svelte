<script lang="ts">
    import { onMount } from'svelte';

    let dataDisplay = '';
    let chunks: Uint8Array[] = [];
    let totalBytesReceived = 0;
    let previousReceiveTime = Date.now();

    async function fetchTimeLineData() {
        try {
            const response = await fetch('https://usa-chat.degpt.ai/api/v0/chat/completion/proxy', {
                method: "POST",
                mode: 'no-cors',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "model": "Llama-3.1-405B",
                    "messages": [
                        {
                        "role": "user",
                        "content": "山西好玩的地方"
                        }
                    ],
                    "stream": false,
                    "project": "DecentralGPT",
                    "max_tokens": 50
                })
            }).then(async (res) => {
                // if (!res.ok) throw await res.json();
                return res;
            });

            // const reader = response.body.getReader();
            console.log("====================", response);

            // return new Promise<void>((resolve, reject) => {
            //     function read() {
            //         return reader.read().then(({ done, value }) => {
            //             const currentReceiveTime = Date.now();
            //             const timeInterval = currentReceiveTime - previousReceiveTime;
            //             previousReceiveTime = currentReceiveTime;

            //             if (done) {
            //                 const text = Buffer.concat(chunks).toString('utf8');
            //                 resolve();
            //             } else {
            //                 chunks.push(value);
            //                 totalBytesReceived += value.byteLength;
            //                 // 实时更新展示数据
            //                 updateDataDisplay(timeInterval, totalBytesReceived);
            //                 read();
            //             }
            //         });
            //     }

            //     read();
            // });
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function updateDataDisplay(timeInterval: number, totalBytesReceived: number) {
        dataDisplay += `Received data block. Time interval: ${timeInterval} ms. Total bytes received: ${totalBytesReceived}\n`;
    }

    onMount(() => {
        
    });
</script>

<main>
    <button on:click = {async() => {fetchTimeLineData()}}>开始请求</button>
    <pre>{dataDisplay}</pre>
</main>