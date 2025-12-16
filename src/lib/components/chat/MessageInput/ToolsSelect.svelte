<script lang="ts">
  import { onMount, getContext } from "svelte";
  import { toolflag, tooltype } from "$lib/stores";
  import { DropdownMenu } from "bits-ui";

  const i18n = getContext("i18n");
  let show = false;

  export let inputplaceholder = "";
  export let tranLang = "";

  let languages = [
    {"code": "de-DE", "tip": "German"},
    {"code": "en-US", "tip": "English"},
    {"code": "es-ES", "tip": "Spanish"},
    {"code": "fr-FR", "tip": "French"},
    {"code": "id-ID", "tip": "Indonesian"},
    {"code": "ja-JP", "tip": "Japanese"},
    {"code": "ko-KR", "tip": "Korean"},
    {"code": "pt-PT", "tip": "Portuguese"},
    {"code": "ru-RU", "tip": "Russian"},
    {"code": "th-TH", "tip": "Thai"},
    {"code": "tr-TR", "tip": "Turkish"},
    {"code": "vi-VN", "tip": "Vietnamese"},
    {"code": "zh-CN", "tip": "Chinese"}
  ];

  let lanindex = 1;
  function changeTranLang(index:number) {
    lanindex = index;
    tranLang = $i18n.t(languages[lanindex].tip);
    show = false;
  }

  onMount(() => {
    let langcode = $i18n.language;
    lanindex = languages.findIndex(item => item.code == langcode);
    tranLang = $i18n.t(languages[lanindex].tip);
  })

</script>

{#if $toolflag && $tooltype != ""}
  <div class="w-full">
    {#if $tooltype == 'bing'}
      <div class="flex justify-between p-4 border-b border-gray-300">
        <div class="flex flex-row items-center">
          <svg  xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1024 1024"
            class="w-[1rem] h-[1rem]"
            fill="currentColor">
            <path d="M911.36 426.666667L433.493333 238.933333c-6.826667-3.413333-13.653333 0-17.066666 3.413334-6.826667 6.826667-6.826667 13.653333-6.826667 20.48l102.4 238.933333 10.24 10.24 146.773333 40.96-416.426666 225.28 116.053333-98.986667c3.413333-3.413333 6.826667-6.826667 6.826667-13.653333V102.4c0-6.826667-3.413333-13.653333-10.24-17.066667L126.293333 0c-6.826667 0-13.653333 0-17.066666 3.413333-3.413333 3.413333-6.826667 6.826667-6.826667 13.653334v853.333333c0 3.413333 0 3.413333 3.413333 6.826667l3.413334 3.413333 3.413333 3.413333 238.933333 136.533334c3.413333 0 6.826667 3.413333 6.826667 3.413333 3.413333 0 6.826667 0 10.24-3.413333l546.133333-341.333334c3.413333-3.413333 6.826667-10.24 6.826667-13.653333V443.733333c0-6.826667-3.413333-13.653333-10.24-17.066666z"/>
          </svg>
          <span class="ml-2">{$i18n.t("Search the Web")}</span>
        </div>
        <button on:click={() => {
          toolflag.set(false);
          tooltype.set("");
          inputplaceholder= "";
        }}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 s-00buWcsF1gFk">
            <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" class="s-00buWcsF1gFk"></path>
          </svg>
        </button>
      </div>
    {:else if $tooltype == 'twitter'}
      <div class="flex justify-between p-4 border-b border-gray-300">
        <div class="flex flex-row items-center">
          <svg xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1024 1024"
            class="w-[1rem] h-[1rem]" 
            fill="currentColor">
            <path d="M761.759375 122h132.320625L605 452.4003125 945.08 902H678.8L470.24 629.3196875 231.599375 902H99.2l309.1996875-353.4L82.16 122h273.0403125l188.52 249.24z m-46.4390625 700.8h73.32L315.359375 197.0403125h-78.680625z"/>
          </svg>
          <span class="ml-2">{$i18n.t("Search the Twitter")}</span>
        </div>
        <button on:click={() => {
          toolflag.set(false);
          tooltype.set("");
          inputplaceholder= "";
        }}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 s-00buWcsF1gFk">
            <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" class="s-00buWcsF1gFk"></path>
          </svg>
        </button>
      </div>
    {:else if $tooltype == 'youtube'}
      <div class="flex justify-between p-4 border-b border-gray-300">
        <div class="flex flex-row items-center">
          <svg xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1024 1024"
            class="w-[1.6rem] h-[1.6rem]" 
            fill="currentColor">
            <path d="M759.466667 187.349333c-55.765333-3.797333-145.493333-6.016-246.272-6.016-99.456 0-191.744 2.261333-246.869334 6.016-178.645333 12.202667-179.285333 156.928-180.096 324.864 0.810667 167.509333 1.450667 312.192 180.138667 324.48 55.253333 3.712 147.669333 5.973333 247.210667 5.973334h0.042666c100.650667 0 190.250667-2.176 245.888-5.973334 178.645333-12.245333 179.285333-156.970667 180.096-324.906666-0.853333-167.552-1.536-312.277333-180.138666-324.437334z m-5.845334 564.181334c-52.949333 3.626667-142.72 5.802667-240.042666 5.802666h-0.042667c-97.706667 0-187.989333-2.176-241.408-5.802666-79.36-5.461333-99.626667-29.696-100.565333-239.317334 0.938667-210.048 21.205333-234.325333 100.565333-239.701333 53.290667-3.669333 143.402667-5.845333 241.024-5.845333 97.450667 0 187.349333 2.176 240.469333 5.845333 79.36 5.376 99.626667 29.610667 100.565334 239.274667-0.938667 210.090667-21.205333 234.325333-100.565334 239.744z"/>
            <path d="M416.896 640l256-128.256-256-127.744z"/>
          </svg>
          <span class="ml-2">{$i18n.t("Search the YouTube")}</span>
        </div>
        <button on:click={() => {
          toolflag.set(false);
          tooltype.set("");
          inputplaceholder= "";
        }}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 s-00buWcsF1gFk">
            <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" class="s-00buWcsF1gFk"></path>
          </svg>
        </button>
      </div>
    {:else if $tooltype == 'translate'}
      <div class="flex flex-col px-4 pt-4 border-b border-gray-300">
        <div class="flex justify-between">
          <div class="flex flex-row items-center">
            <svg xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 1024 1024"
              class="w-[1.2rem] h-[1.2rem]" 
              fill="currentColor">
              <path d="M284.288 33.664l2.858667 3.712c19.456 25.386667 37.290667 55.424 53.504 89.941333h210.346666v70.058667h-84.821333c-25.813333 78.848-62.762667 145.322667-110.933333 199.722667 55.125333 42.752 123.136 78.506667 203.690666 108.202666l7.552 2.773334-39.125333 60.032-4.821333-1.834667c-86.485333-32.426667-158.933333-72.32-217.216-119.765333-61.696 53.333333-137.173333 92.757333-225.706667 117.76l-4.693333 1.28L37.12 503.466667l8.362667-2.133334c84.138667-21.717333 154.069333-55.125333 209.621333-100.565333a496.384 496.384 0 0 1-119.210667-203.349333h-85.333333V127.317333h213.418667a395.946667 395.946667 0 0 0-44.458667-60.928l-6.186667-7.04L284.288 33.706667zM608 102.4a38.4 38.4 0 0 1 38.4-38.4h147.2a166.4 166.4 0 0 1 166.4 166.4v121.6a38.4 38.4 0 1 1-76.8 0V230.4a89.6 89.6 0 0 0-89.6-89.6h-147.2a38.4 38.4 0 0 1-38.4-38.4zM204.757333 197.376A429.653333 429.653333 0 0 0 304.896 352.853333c38.314667-43.605333 67.882667-95.573333 88.32-155.477333H204.757333z m528.512 218.325333a19.2 19.2 0 0 1 18.005334-12.501333h7.808a19.2 19.2 0 0 1 18.005333 12.501333l195.285333 524.8a19.2 19.2 0 0 1-18.005333 25.898667h-36.650667a19.2 19.2 0 0 1-18.005333-12.586667l-51.669333-141.013333h-185.685334l-51.669333 141.013333a19.2 19.2 0 0 1-18.048 12.586667h-36.650667a19.2 19.2 0 0 1-17.962666-25.898667l195.242666-524.8z m-42.794666 320.298667h129.408L755.2 559.402667l-64.725333 176.597333zM64 672a38.4 38.4 0 0 1 76.8 0v121.6c0 49.493333 40.106667 89.6 89.6 89.6h160a38.4 38.4 0 0 1 0 76.8H230.4a166.4 166.4 0 0 1-166.4-166.4v-121.6z"/>
            </svg>
            <span class="ml-2">{$i18n.t("Translate")}</span>
          </div>
          <button on:click={() => {
            toolflag.set(false);
            tooltype.set("");
            inputplaceholder= "";
          }}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 s-00buWcsF1gFk">
              <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" class="s-00buWcsF1gFk"></path>
            </svg>
          </button>
        </div>
        <div class="flex flex-row items-center pt-3 pb-2">
          <div class="text-sm border border-gray-500 px-3 py-2 rounded-lg">{$i18n.t("Auto-detect")}</div>
          <svg xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 1024 1024" 
            version="1.1"
            class="w-[1.6rem] h-[1.6rem] mx-2" 
            fill="currentColor">
            <path d="M951.127 483.716L668.284 200.873c-7.811-7.811-18.048-11.716-28.284-11.716-10.237 0-20.474 3.905-28.284 11.716-15.621 15.621-15.621 40.947 0 56.568L826.274 472H104c-22.092 0-40 17.908-40 40 0 22.091 17.908 40 40 40h722.274L611.716 766.559c-15.621 15.62-15.621 40.947 0 56.568 7.811 7.811 18.047 11.716 28.284 11.716 10.236 0 20.474-3.905 28.284-11.716l282.843-282.843c15.621-15.621 15.621-40.948 0-56.568z"/>
          </svg>
          <DropdownMenu.Root bind:open={show}>
            <DropdownMenu.Trigger>
              <div class="flex flex-row">
                <button class="flex flex-row text-sm border border-gray-500 px-3 py-2 rounded-lg"
                  on:click={(e) => {
                    e.preventDefault();
                  }}>
                  <span class="text-sm mr-1">{$i18n.t(languages[lanindex].tip)}</span>
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="self-center ml-1 size-5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5"/>
                  </svg>
                </button>
              </div>
            </DropdownMenu.Trigger>
            <DropdownMenu.Content side="top">
              <slot>
                <div class="flex flex-col bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 
                  dark:text-gray-300 text-gray-700 shadow-lg px-3 py-3 rounded-2xl mb-1">
                  {#each languages as langitem, index}
                    <button
                    aria-label="model-item"
                      class="flex item-center w-full text-left font-medium line-clamp-1 select-none items-center rounded-button px-2 py-1
                        hover:bg-gray-100 dark:hover:bg-gray-850 rounded-lg cursor-pointer data-[highlighted]:bg-muted"
                      on:click={(e) => {
                        e.preventDefault();
                        changeTranLang(index);
                      }}
                    >
                      <span class="text-sm ml-1">{$i18n.t(langitem.tip)}</span>
                    </button>
                  {/each}
                </div>
              </slot>
            </DropdownMenu.Content>
          </DropdownMenu.Root>
        </div>
      </div>
      
    {:else if $tooltype == 'webread'}
      <div class="flex justify-between p-4 border-b border-gray-300">
        <div class="flex flex-row items-center">
          <svg xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 1035 1024"
            class="w-[1rem] h-[1rem]" 
            fill="currentColor">
            <path d="M132.201313 0h768.560175c73.943107 0 134.442013 60.498906 134.442013 132.201313v757.356674c0 73.943107-60.498906 134.442013-134.442013 134.442013H132.201313c-71.702407 0-132.201313-60.498906-132.201313-134.442013V132.201313C0 60.498906 60.498906 0 132.201313 0z m96.350109 80.665208H132.201313c-26.888403 0-51.536105 24.647702-51.536105 51.536105v757.356674c0 29.129103 24.647702 51.536105 51.536105 51.536105h768.560175c29.129103 0 51.536105-22.407002 51.536105-51.536105V132.201313c0-26.888403-22.407002-51.536105-51.536105-51.536105H228.551422z"/>
            <path d="M165.811816 203.90372h714.436061v54.363869H165.811816zM165.811816 369.715536h714.436061v54.363869H165.811816zM604.989059 611.71116h274.382705v54.363868H604.989059zM604.989059 775.282276h274.382705v54.363868H604.989059zM257.680525 546.730853h163.571116c51.536105 0 94.109409 42.573304 94.109409 91.868709v165.811817c0 51.536105-42.573304 91.868709-94.109409 91.868709h-163.571116c-51.536105 0-91.868709-40.332604-91.868709-91.868709v-165.811817c0-49.295405 40.332604-91.868709 91.868709-91.868709z m26.888403 56.017506h112.035011c33.610503 0 60.498906 29.129103 60.498906 62.739606v112.035011c0 33.610503-26.888403 62.739606-60.498906 62.739606h-112.035011c-35.851204 0-62.739606-29.129103-62.739606-62.739606v-112.035011c0-33.610503 26.888403-62.739606 62.739606-62.739606z"/>
          </svg>
          <span class="ml-2">{$i18n.t("Webpage Reading")}</span>
        </div>
        <button on:click={() => {
          toolflag.set(false);
          tooltype.set("");
          inputplaceholder= "";
        }}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 s-00buWcsF1gFk">
            <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" class="s-00buWcsF1gFk"></path>
          </svg>
        </button>
      </div>
    {/if}
  </div>
{/if}