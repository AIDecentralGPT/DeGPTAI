<script lang="ts">
    // 接收推文数据
    export let data;

    function formatText(text:string) {
        const formattedText = text.replace(/\n/g, '<br>');
        const urlRegex = /https?:\/\/[^\s]+/g;
        return formattedText.replace(urlRegex, '');;
    }

    function formatDateToTwitterStyle(dateInput:string) {
        // 如果传入的不是 Date 对象，则尝试转换为 Date 对象
        const date = typeof dateInput === 'object'? dateInput : new Date(dateInput);
        if (isNaN(date.getTime())) {
            throw new Error('输入的日期格式无效');
        }

        // 格式化时间部分
        const timeOptions = {
            hour: 'numeric',
            minute: 'numeric',
            hour12: true
        };
        const timeFormatter = new Intl.DateTimeFormat('en-US', timeOptions);
        const formattedTime = timeFormatter.format(date);

        // 格式化日期部分
        const dateOptions = {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        };
        const dateFormatter = new Intl.DateTimeFormat('en-US', dateOptions);
        let formattedDate = dateFormatter.format(date);
        // 替换逗号为点号
        formattedDate = formattedDate.replace(',', '.');

        // 组合时间和日期部分
        return `${formattedTime} · ${formattedDate}`;
    }

</script>

<div class="w-[320px] p-4 rounded-xl bg-gray-50 dark:bg-gray-900 border-[1px] border-inherit dark:border-gray-600">
    <a href="https://x.com/{data.screen_name}/status/{data.id_str}" target="_blank">
        <div class="flex justify-between">
            <div class="flex flex-row items-center mr-2">
                <img class="rounded-full" src="{data.profile_image_url_https}" alt="" draggable="false"/>
                <div class="flex flex-col ml-1">
                    <span class="text-sm font-black whitespace-nowrap overflow-hidden text-ellipsis w-[200px]">{data.name}</span>
                    <div>
                        <span class="text-sm">@{data.screen_name}</span>
                        <span> · </span>
                        <span class="text-sm font-bold text-[#006FD6]">Follow</span>
                    </div>
                </div>
            </div>
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" 
                    viewBox="0 0 1024 1024" 
                    class="w-[1.6rem] h-[1.6rem]" 
                    fill="currentColor">
                    <path d="M761.759375 122h132.320625L605 452.4003125 945.08 902H678.8L470.24 629.3196875 231.599375 902H99.2l309.1996875-353.4L82.16 122h273.0403125l188.52 249.24z m-46.4390625 700.8h73.32L315.359375 197.0403125h-78.680625z"/>
                </svg>
            </div>
        </div>
        <div class="text-sm mt-2">{@html formatText(data.full_text)}</div>
        {#if data?.media_url_https}
            <img class="w-full h-[320px] object-cover mt-2 rounded-xl" src={data?.media_url_https} alt="" draggable="false"/>
        {/if}
        <div class="text-sm mt-2 dark:text-gray-600">{formatDateToTwitterStyle(data.tweet_created_at)}</div>
        <hr class="my-2 dark:border-gray-600"/>
        <div class="flex justify-between items-center">
            <div class="flex flex-row items-center">
                <svg viewBox="0 0 24 24" aria-hidden="true" class="w-[1.3rem] h-[1.3rem]" fill="#F91880">
                    <g>
                        <path d="M20.884 13.19c-1.351 2.48-4.001 5.12-8.379 7.67l-.503.3-.504-.3c-4.379-2.55-7.029-5.19-8.382-7.67-1.36-2.5-1.41-4.86-.514-6.67.887-1.79 2.647-2.91 4.601-3.01 1.651-.09 3.368.56 4.798 2.01 1.429-1.45 3.146-2.1 4.796-2.01 1.954.1 3.714 1.22 4.601 3.01.896 1.81.846 4.17-.514 6.67z"></path>
                    </g>
                </svg>
                {#if data?.favorite_count != 0}
                    <span class="text-sm font-black dark:text-gray-600 ml-1">{data.favorite_count}</span>
                {/if}
            </div>
            <div class="flex flex-row items-center">
                <svg viewBox="0 0 24 24" aria-hidden="true" class="w-[1.2rem] h-[1.2rem]" fill="#1D9BF0">
                    <g>
                        <path d="M1.751 10c0-4.42 3.584-8 8.005-8h4.366c4.49 0 8.129 3.64 8.129 8.13 0 2.96-1.607 5.68-4.196 7.11l-8.054 4.46v-3.69h-.067c-4.49.1-8.183-3.51-8.183-8.01z"></path>
                    </g>
                </svg>
                <span class="text-sm font-black ml-1 dark:text-gray-600">Reply</span>
            </div>
            <div class="flex flex-row items-center mr-10">
                <svg viewBox="0 0 24 24" aria-hidden="true" class="w-[1.2rem] h-[1.2rem] dark:fill-gray-600">
                    <g>
                        <path d="M18.36 5.64c-1.95-1.96-5.11-1.96-7.07 0L9.88 7.05 8.46 5.64l1.42-1.42c2.73-2.73 7.16-2.73 9.9 0 2.73 2.74 2.73 7.17 0 9.9l-1.42 1.42-1.41-1.42 1.41-1.41c1.96-1.96 1.96-5.12 0-7.07zm-2.12 3.53l-7.07 7.07-1.41-1.41 7.07-7.07 1.41 1.41zm-12.02.71l1.42-1.42 1.41 1.42-1.41 1.41c-1.96 1.96-1.96 5.12 0 7.07 1.95 1.96 5.11 1.96 7.07 0l1.41-1.41 1.42 1.41-1.42 1.42c-2.73 2.73-7.16 2.73-9.9 0-2.73-2.74-2.73-7.17 0-9.9z"></path>
                    </g>
                </svg>
                <span class="text-sm font-black ml-1 dark:text-gray-600">Copy link</span>
            </div>
        </div>
        <div class="flex justify-center items-center w-full h-[35px] rounded-full mt-2 border-[1px] border-inherit dark:border-gray-600 text-sm font-black text-[#006FD6]"> Read more on X</div>
    </a>
</div>