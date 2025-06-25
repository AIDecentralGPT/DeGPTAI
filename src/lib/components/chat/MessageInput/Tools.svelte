<script lang="ts">
  import { DropdownMenu } from "bits-ui";
  import { onMount, getContext } from "svelte";
  const i18n = getContext("i18n");

  let show = false;
  let button:HTMLElement;
  let buttonWidth:number;
  let resizeObserver: ResizeObserver;

  export let inputplaceholder = "";
  export let search = false;
  export let type = "";

  onMount(() => {
    resizeObserver = new ResizeObserver((entries) => {
      buttonWidth = entries[0].contentRect.width;
    });
    if (button) {
      resizeObserver.observe(button);
    }
    return () => {
      if (resizeObserver) resizeObserver.disconnect();
    };
  });

</script>

<DropdownMenu.Root bind:open={show}>
  <DropdownMenu.Trigger>
    <div class="flex flex-row">
      <button bind:this={button} class="flex flex-row items-center primaryButton rounded-full p-1.5"
        on:click={(e) => {
          e.preventDefault();
        }}>
        <svg viewBox="0 0 20 20" fill="#FFFFFF" xmlns="http://www.w3.org/2000/svg" aria-label="" class="w-[1.2rem] h-[1.2rem] mx-0.8">
          <path d="M7.91626 11.0013C9.43597 11.0013 10.7053 12.0729 11.011 13.5013H16.6663L16.801 13.515C17.1038 13.5771 17.3311 13.8453 17.3313 14.1663C17.3313 14.4875 17.1038 14.7555 16.801 14.8177L16.6663 14.8314H11.011C10.7056 16.2601 9.43619 17.3314 7.91626 17.3314C6.39643 17.3312 5.1269 16.2601 4.82153 14.8314H3.33325C2.96598 14.8314 2.66821 14.5336 2.66821 14.1663C2.66839 13.7992 2.96609 13.5013 3.33325 13.5013H4.82153C5.12713 12.0729 6.39665 11.0015 7.91626 11.0013ZM7.91626 12.3314C6.90308 12.3316 6.08148 13.1532 6.0813 14.1663C6.0813 15.1797 6.90297 16.0011 7.91626 16.0013C8.9297 16.0013 9.75122 15.1798 9.75122 14.1663C9.75104 13.153 8.92959 12.3314 7.91626 12.3314ZM12.0833 2.66829C13.6031 2.66829 14.8725 3.73966 15.178 5.16829H16.6663L16.801 5.18196C17.1038 5.24414 17.3313 5.51212 17.3313 5.83333C17.3313 6.15454 17.1038 6.42253 16.801 6.4847L16.6663 6.49837H15.178C14.8725 7.92701 13.6031 8.99837 12.0833 8.99837C10.5634 8.99837 9.29405 7.92701 8.98853 6.49837H3.33325C2.96598 6.49837 2.66821 6.2006 2.66821 5.83333C2.66821 5.46606 2.96598 5.16829 3.33325 5.16829H8.98853C9.29405 3.73966 10.5634 2.66829 12.0833 2.66829ZM12.0833 3.99837C11.0698 3.99837 10.2483 4.81989 10.2483 5.83333C10.2483 6.84677 11.0698 7.66829 12.0833 7.66829C13.0967 7.66829 13.9182 6.84677 13.9182 5.83333C13.9182 4.81989 13.0967 3.99837 12.0833 3.99837Z"/>
        </svg>
        <span class="text-xs text-white mr-1">{$i18n.t("Tool")}</span>
      </button>
    </div>
  </DropdownMenu.Trigger>
  <DropdownMenu.Content side="right">
    <slot>
      <div class="flex flex-col bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 
        dark:text-gray-300 text-gray-700 shadow-lg px-3 py-5 rounded-2xl mb-14"
        style="margin-left:-{Math.trunc(buttonWidth + 15)}px;">
        <button
          aria-label="model-item"
          class="flex item-center w-full text-left font-medium line-clamp-1 select-none items-center rounded-button p-2 
            hover:bg-gray-100 dark:hover:bg-gray-850 rounded-xl cursor-pointer data-[highlighted]:bg-muted"
          on:click={(e) => {
            e.preventDefault();
            search = true;
            type="bing"
            inputplaceholder = "";
            show = false;
          }}
        >
          <div class="flex flex-row items-center gap-2 mr-1">
            <svg  xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 1024 1024"
              class="w-[0.8rem] h-[0.8rem]"
              fill="currentColor">
              <path d="M911.36 426.666667L433.493333 238.933333c-6.826667-3.413333-13.653333 0-17.066666 3.413334-6.826667 6.826667-6.826667 13.653333-6.826667 20.48l102.4 238.933333 10.24 10.24 146.773333 40.96-416.426666 225.28 116.053333-98.986667c3.413333-3.413333 6.826667-6.826667 6.826667-13.653333V102.4c0-6.826667-3.413333-13.653333-10.24-17.066667L126.293333 0c-6.826667 0-13.653333 0-17.066666 3.413333-3.413333 3.413333-6.826667 6.826667-6.826667 13.653334v853.333333c0 3.413333 0 3.413333 3.413333 6.826667l3.413334 3.413333 3.413333 3.413333 238.933333 136.533334c3.413333 0 6.826667 3.413333 6.826667 3.413333 3.413333 0 6.826667 0 10.24-3.413333l546.133333-341.333334c3.413333-3.413333 6.826667-10.24 6.826667-13.653333V443.733333c0-6.826667-3.413333-13.653333-10.24-17.066666z"/>
            </svg>
            <span class="text-sm ml-1">{$i18n.t("Search the Web")}</span>
          </div>
        </button>
        <button
          aria-label="model-item"
          class="flex item-center w-full text-left font-medium line-clamp-1 select-none items-center rounded-button p-2 
            hover:bg-gray-100 dark:hover:bg-gray-850 rounded-xl cursor-pointer data-[highlighted]:bg-muted"
          on:click={(e) => {
            e.preventDefault();
            search = true;
            type = "twitter";
            inputplaceholder = "";
            show = false;
          }}
        >
          <div class="flex flex-row items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 1024 1024"
              class="w-[0.8rem] h-[0.8rem]" 
              fill="currentColor">
              <path d="M761.759375 122h132.320625L605 452.4003125 945.08 902H678.8L470.24 629.3196875 231.599375 902H99.2l309.1996875-353.4L82.16 122h273.0403125l188.52 249.24z m-46.4390625 700.8h73.32L315.359375 197.0403125h-78.680625z"/>
            </svg>
            <span class="text-sm ml-1">{$i18n.t("Search the Twitter")}</span>
          </div>
        </button>
        <button
          aria-label="model-item"
          class="flex item-center w-full text-left font-medium line-clamp-1 select-none items-center rounded-button p-2 
            hover:bg-gray-100 dark:hover:bg-gray-850 rounded-xl cursor-pointer data-[highlighted]:bg-muted"
          on:click={(e) => {
            e.preventDefault();
            search = true;
            type="youtube";
            inputplaceholder = "";
            show = false;
          }}
        >
          <div class="flex flex-row items-center gap-2 pr-10">
            <svg xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 1024 1024"
              class="w-[1rem] h-[1rem]" 
              fill="currentColor">
              <path d="M759.466667 187.349333c-55.765333-3.797333-145.493333-6.016-246.272-6.016-99.456 0-191.744 2.261333-246.869334 6.016-178.645333 12.202667-179.285333 156.928-180.096 324.864 0.810667 167.509333 1.450667 312.192 180.138667 324.48 55.253333 3.712 147.669333 5.973333 247.210667 5.973334h0.042666c100.650667 0 190.250667-2.176 245.888-5.973334 178.645333-12.245333 179.285333-156.970667 180.096-324.906666-0.853333-167.552-1.536-312.277333-180.138666-324.437334z m-5.845334 564.181334c-52.949333 3.626667-142.72 5.802667-240.042666 5.802666h-0.042667c-97.706667 0-187.989333-2.176-241.408-5.802666-79.36-5.461333-99.626667-29.696-100.565333-239.317334 0.938667-210.048 21.205333-234.325333 100.565333-239.701333 53.290667-3.669333 143.402667-5.845333 241.024-5.845333 97.450667 0 187.349333 2.176 240.469333 5.845333 79.36 5.376 99.626667 29.610667 100.565334 239.274667-0.938667 210.090667-21.205333 234.325333-100.565334 239.744z"/>
              <path d="M416.896 640l256-128.256-256-127.744z"/>
            </svg>
            <span class="text-sm ml-1">{$i18n.t("Search the YouTube")}</span>
          </div>
        </button>
        <button
          aria-label="model-item"
          class="flex item-center w-full text-left font-medium line-clamp-1 select-none items-center rounded-button p-2 
            hover:bg-gray-100 dark:hover:bg-gray-850 rounded-xl cursor-pointer data-[highlighted]:bg-muted"
          on:click={(e) => {
            e.preventDefault();
            search = true;
            type="translate";
            inputplaceholder= $i18n.t("Enter text to translate...");
            show = false;
          }}
        >
          <div class="flex flex-row items-center gap-2 pr-10">
            <svg xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 1024 1024"
              class="w-[1rem] h-[1rem]" 
              fill="currentColor">
              <path d="M284.288 33.664l2.858667 3.712c19.456 25.386667 37.290667 55.424 53.504 89.941333h210.346666v70.058667h-84.821333c-25.813333 78.848-62.762667 145.322667-110.933333 199.722667 55.125333 42.752 123.136 78.506667 203.690666 108.202666l7.552 2.773334-39.125333 60.032-4.821333-1.834667c-86.485333-32.426667-158.933333-72.32-217.216-119.765333-61.696 53.333333-137.173333 92.757333-225.706667 117.76l-4.693333 1.28L37.12 503.466667l8.362667-2.133334c84.138667-21.717333 154.069333-55.125333 209.621333-100.565333a496.384 496.384 0 0 1-119.210667-203.349333h-85.333333V127.317333h213.418667a395.946667 395.946667 0 0 0-44.458667-60.928l-6.186667-7.04L284.288 33.706667zM608 102.4a38.4 38.4 0 0 1 38.4-38.4h147.2a166.4 166.4 0 0 1 166.4 166.4v121.6a38.4 38.4 0 1 1-76.8 0V230.4a89.6 89.6 0 0 0-89.6-89.6h-147.2a38.4 38.4 0 0 1-38.4-38.4zM204.757333 197.376A429.653333 429.653333 0 0 0 304.896 352.853333c38.314667-43.605333 67.882667-95.573333 88.32-155.477333H204.757333z m528.512 218.325333a19.2 19.2 0 0 1 18.005334-12.501333h7.808a19.2 19.2 0 0 1 18.005333 12.501333l195.285333 524.8a19.2 19.2 0 0 1-18.005333 25.898667h-36.650667a19.2 19.2 0 0 1-18.005333-12.586667l-51.669333-141.013333h-185.685334l-51.669333 141.013333a19.2 19.2 0 0 1-18.048 12.586667h-36.650667a19.2 19.2 0 0 1-17.962666-25.898667l195.242666-524.8z m-42.794666 320.298667h129.408L755.2 559.402667l-64.725333 176.597333zM64 672a38.4 38.4 0 0 1 76.8 0v121.6c0 49.493333 40.106667 89.6 89.6 89.6h160a38.4 38.4 0 0 1 0 76.8H230.4a166.4 166.4 0 0 1-166.4-166.4v-121.6z"/>
            </svg>
            <span class="text-sm ml-1">{$i18n.t("Translate")}</span>
          </div>
        </button>
        <button
          aria-label="model-item"
          class="flex item-center w-full text-left font-medium line-clamp-1 select-none items-center rounded-button p-2 
            hover:bg-gray-100 dark:hover:bg-gray-850 rounded-xl cursor-pointer data-[highlighted]:bg-muted"
          on:click={(e) => {
            e.preventDefault();
            search = true;
            type="webread";
            inputplaceholder = $i18n.t("Paste or enter a link...");
            show = false;
          }}
        >
          <div class="flex flex-row items-center gap-2 pr-10">
            <svg xmlns="http://www.w3.org/2000/svg" 
              viewBox="0 0 1035 1024"
              class="w-[1rem] h-[1rem]" 
              fill="currentColor">
              <path d="M132.201313 0h768.560175c73.943107 0 134.442013 60.498906 134.442013 132.201313v757.356674c0 73.943107-60.498906 134.442013-134.442013 134.442013H132.201313c-71.702407 0-132.201313-60.498906-132.201313-134.442013V132.201313C0 60.498906 60.498906 0 132.201313 0z m96.350109 80.665208H132.201313c-26.888403 0-51.536105 24.647702-51.536105 51.536105v757.356674c0 29.129103 24.647702 51.536105 51.536105 51.536105h768.560175c29.129103 0 51.536105-22.407002 51.536105-51.536105V132.201313c0-26.888403-22.407002-51.536105-51.536105-51.536105H228.551422z"/>
              <path d="M165.811816 203.90372h714.436061v54.363869H165.811816zM165.811816 369.715536h714.436061v54.363869H165.811816zM604.989059 611.71116h274.382705v54.363868H604.989059zM604.989059 775.282276h274.382705v54.363868H604.989059zM257.680525 546.730853h163.571116c51.536105 0 94.109409 42.573304 94.109409 91.868709v165.811817c0 51.536105-42.573304 91.868709-94.109409 91.868709h-163.571116c-51.536105 0-91.868709-40.332604-91.868709-91.868709v-165.811817c0-49.295405 40.332604-91.868709 91.868709-91.868709z m26.888403 56.017506h112.035011c33.610503 0 60.498906 29.129103 60.498906 62.739606v112.035011c0 33.610503-26.888403 62.739606-60.498906 62.739606h-112.035011c-35.851204 0-62.739606-29.129103-62.739606-62.739606v-112.035011c0-33.610503 26.888403-62.739606 62.739606-62.739606z"/>
            </svg>
            <span class="text-sm ml-1">{$i18n.t("Webpage Reading")}</span>
          </div>
        </button>
      </div>
    </slot>
  </DropdownMenu.Content>
</DropdownMenu.Root>