<script>
  import { getContext } from "svelte";
  import { checkUniapp } from "$lib/utils";
  import {
    downLoadUrl,
    showDownLoad
  } from "$lib/stores";
  const i18n = getContext("i18n");
</script>

<section>
  <div class="flex justify-between gap-6 px-3 pt-2 pb-1">
    <div class="text-sm leading-6">{$i18n.t('Join Our Community')}:</div>

    <div class="flex gap-6 items-center">
      <button
        on:click={() => {
          if (checkUniapp()) {
            $downLoadUrl = "https://x.com/DecentralGPT";
            $showDownLoad = true;
          } else {
            window.open("https://x.com/DecentralGPT", "_blank");
          }
        }}
      ><svg
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        fill="none"
        version="1.1"
        width="14"
        height="16"
        viewBox="0 0 16 14"
        ><defs
          ><clipPath id="master_svg0_3_1076"
            ><rect x="0" y="0" width="16" height="14" rx="0" /></clipPath
          ></defs
        ><g clip-path="url(#master_svg0_3_1076)"
          ><g
            ><path
              d="M12.0818,0L14.4341,0L9.29493,5.93026L15.3408,14L10.6069,14L6.8992,9.10574L2.6567,14L0.302933,14L5.79982,7.65692L0,0L4.85405,0L8.20552,4.47354L12.0818,0ZM11.2562,12.5785L12.5597,12.5785L4.14577,1.34688L2.747,1.34688L11.2562,12.5785Z"
              fill="currentColor"
              fill-opacity="1"
            /></g
          ></g
        ></svg
      ></button>
      <button
        on:click={() => {
          if (checkUniapp()) {
            $downLoadUrl = "https://t.me/DecentralGPT";
            $showDownLoad = true;
          } else {
            window.open("https://t.me/DecentralGPT", "_blank");
          }
        }}
      ><svg
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        fill="none"
        version="1.1"
        width="16"
        height="16"
        viewBox="0 0 18 14"
        ><defs
          ><clipPath id="master_svg0_1_11376"
            ><rect x="0" y="0" width="18" height="14" rx="0" /></clipPath
          ></defs
        ><g clip-path="url(#master_svg0_1_11376)"
          ><g
            ><path
              d="M16.4654,0.1236C16.4654,0.1236,18.1306,-0.482411,17.9918,0.989313C17.9455,1.59532,17.5293,3.71631,17.2055,6.01048C17.2055,6.01048,16.0954,12.8063,16.0954,12.8063C16.0954,12.8063,16.0029,13.8019,15.1703,13.9751C14.3377,14.1482,13.0889,13.3691,12.8576,13.1959C12.6726,13.0661,9.38863,11.1182,8.23227,10.1659C7.90847,9.90619,7.53845,9.38674,8.27852,8.78075C8.27852,8.78075,13.1352,4.45219,13.1352,4.45219C13.6902,3.93276,14.2453,2.72076,11.9326,4.19248C11.9326,4.19248,5.45706,8.30464,5.45706,8.30464C5.45706,8.30464,4.71699,8.73748,3.3294,8.34792C3.3294,8.34792,0.322899,7.4822,0.322899,7.4822C0.322899,7.4822,-0.787195,6.83292,1.10919,6.18359C5.73459,4.14915,11.4238,2.07144,16.4654,0.1236Z"
              fill="currentColor"
              fill-opacity="1"
            /></g
          ></g
        ></svg
      ></button>
      <button
        on:click={() => {
          if (checkUniapp()) {
            $downLoadUrl = "https://medium.com/@DecentralGPT";
            $showDownLoad = true;
          } else {
            window.open("https://medium.com/@DecentralGPT", "_blank");
          }
        }}
      ><svg
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        fill="none"
        version="1.1"
        width="16"
        height="16"
        viewBox="0 0 18 14"
        ><defs
          ><clipPath id="master_svg0_3_1080"
            ><rect x="0" y="0" width="18" height="14" rx="0" /></clipPath
          ></defs
        ><g clip-path="url(#master_svg0_3_1080)"
          ><g
            ><path
              d="M16.5633,1.63607L18,0.293945L18,0L13.0242,0L9.47813,8.6224L5.44453,0L0.227344,0L0.227344,0.293945L1.90547,2.26725C2.06953,2.41309,2.15391,2.62728,2.13281,2.84147L2.13281,10.5957C2.18438,10.876,2.09297,11.1608,1.89141,11.3636L0,13.6035L0,13.8929L5.35781,13.8929L5.35781,13.599L3.46875,11.3659C3.26484,11.1631,3.16641,10.8805,3.20859,10.598L3.20859,3.88965L7.9125,13.8975L8.45859,13.8975L12.5039,3.88965L12.5039,11.8626C12.5039,12.0723,12.5039,12.1156,12.3633,12.2546L10.9078,13.6286L10.9078,13.9225L17.9672,13.9225L17.9672,13.6286L16.5633,12.2865C16.4414,12.1953,16.3781,12.0426,16.4039,11.8945L16.4039,2.02799C16.3781,1.87988,16.4414,1.72721,16.5633,1.63607Z"
              fill="currentColor"
              fill-opacity="1"
            /></g
          ></g
        ></svg
      ></button>
    </div>
  </div>
</section>
