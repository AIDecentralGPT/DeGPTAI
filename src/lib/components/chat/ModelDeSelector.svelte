<script lang="ts">
  import { getContext } from "svelte";
  import { mobile, deApiBaseUrl } from "$lib/stores";
  import CheckRegion from "$lib/components/icons/CheckRegion.svelte";
  import { getDeBaseUrls } from "$lib/apis/de/index"
  import Modal from '../common/Modal.svelte';

  const i18n = getContext("i18n");

  let show = false;

  let selDeUrl: string = "";

  $: if(show) {
    selDeUrl = $deApiBaseUrl?.name;
  }

  async function assignDeUrl(name: string) {
    selDeUrl = name;
  }
  
  async function changeDeUrl() {
    const deUrls = await getDeBaseUrls();
    const selDeUrlObj = deUrls.find((item) => item.name === selDeUrl);
    deApiBaseUrl.set(selDeUrlObj);
    show = false;
  }
</script>

<div>
  <button class="flex flex-row items-center cursor-pointer"
    on:click={() => {
      show = true;
    }}>
    <svg class="icon region-fill-color" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="30" height="30">
      <path d="M947.108756 511.648694c0-240.108606-194.801924-434.755236-435.1032-434.755236-240.305873 0-435.111994 194.64663-435.111994 434.755236 0 221.801619 166.222901 404.794749 380.984293 431.422296 12.106792 2.55127 26.852794 4.038062 44.415686 4.038062 4.930457 0 9.685034-0.259424 14.27692-0.729505C754.768563 943.931606 947.108756 750.242528 947.108756 511.648694zM884.893338 517.799924c-1.251751-21.692093-4.117408-42.925497-8.48125-63.560906 0.387337-7.368204 0.492666-14.349071 0.2952-20.839071 5.396141 25.231293 8.241812 51.407945 8.241812 78.248547C884.9499 513.703701 884.926516 515.752712 884.893338 517.799924zM139.053218 511.648694c0-26.351534 2.74374-52.061502 7.95021-76.867284 16.10568 17.224122 54.066743 16.817798 63.324466-8.917554 16.564569 9.871507 38.824677 11.669088 38.824677 31.400111 0 65.118849 2.319028 134.932116 61.48951 136.010585 1.66607 0.021785 32.998427 11.87355 47.909917 50.543531 5.155904 13.365538 25.549677 0 47.914314 0 11.16483 0 0 18.808248 0 59.480272 0 40.514331 87.352575 102.896636 87.352575 102.896636-0.404726 26.818217 0.696328 48.503115 2.928215 65.827569-19.717432-0.362954-36.334165 2.250074-49.388714 6.693662C272.196747 848.12916 139.053218 695.432289 139.053218 511.648694zM603.819307 872.916555c-1.933289-9.465183-10.391954-14.648468-25.824691-10.592418 12.313851-52.435848 18.300192-81.808734 44.006564-104.111013 37.193383-32.239142 4.428997-68.090635-23.874013-63.865499-22.307875 3.367717-8.210433-27.618874-28.121134-29.332712-19.910701-1.66607-45.912871-41.267221-74.568443-54.893982-15.189901-7.213309-30.11798-26.544003-53.544497-27.410016-20.763722-0.805054-51.107949 17.555897-51.107949 3.402493 0-45.588091-4.61627-78.118835-5.565027-91.110227-0.766081-10.437323-6.822974-3.515616 21.245995-2.841074 15.276243 0.409123 7.814302-30.681998 22.93465-31.896174 14.850531-1.175003 50.237539 13.900975 59.253226 7.892249 8.375721-5.595206 61.567857 139.617739 61.567857 24.003126 0-13.718099-7.104983-37.568728 0-50.56092 28.099349-51.339991 54.405313-93.181823 52.042915-99.302673-1.340691-3.446064-28.747909-6.291534-50.677241 1.066277-7.400782 2.471125 2.353804 14.061866-8.275589 16.537388-39.825598 9.193567-75.012541-10.73772-62.690696-29.472018 12.617645-19.199982 58.334849-8.375322 62.342532-46.893007 2.305837-22.062841 4.216541-47.615317 5.495274-66.606441 53.59926 8.381317 47.69926-69.55724-31.998305-77.899584 161.233284 1.886321 297.86145 106.006727 347.998057 250.511153-2.535881-2.312632-5.485881-3.718479-8.892971-4.061446-24.096063-60.184395-82.583209-16.628726-62.74306 36.455483-106.305525 81.712999-79.094174 138.703759-44.167654 171.339032 18.378539 17.155369 35.900659 42.956076 47.309324 61.485713-12.417581 36.205653 45.75278 21.707682 74.441329-39.73446C833.914302 741.574005 732.115122 840.463158 603.819307 872.916555z"></path>
    </svg>
    <span class="text-base region-text-color font-bold ml-1">{$i18n.t("Connected to")}</span>
    <span class="text-base region-text-color font-bold ml-1">({$i18n.t($deApiBaseUrl?.name)})</span>
    <span class="text-base region-text-color font-bold ml-1">{$i18n.t("node")}</span>
  </button>
  <Modal bind:show>
    <div class="w-full mt-5 mb-5">
      <div class="flex flex-row w-full region-text-color text-xl text-center">
        <div class="w-full"><span class="ml-6">{$i18n.t("Region Setting")}</span></div>
        <button
          class="self-center mr-4"
          on:click={() => {
            show = false;
          }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            class="w-5 h-5"
          >
            <path
              d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
            />
          </svg>
        </button>
      </div>
      <div class="px-5">
        <button class="flex flex-row items-center w-full region-text-color my-2 select-none data-[highlighted]:bg-muted"
          on:click = { async () => {
            await assignDeUrl("America");
          }}>
          <CheckRegion checkFlag = { selDeUrl === 'America'}/>
          <span class="ml-2">{$i18n.t("America")}</span>
        </button>
        <button class="flex flex-row items-center w-full region-text-color my-2 select-none data-[highlighted]:bg-muted"
          on:click = { async () => {
            await assignDeUrl("Singapore");
          }}>
          <CheckRegion checkFlag = { selDeUrl === 'Singapore'}/>
          <span class="ml-2">{$i18n.t("Singapore")}</span>
        </button>
        <button class="flex flex-row items-center w-full region-text-color my-2 select-none data-[highlighted]:bg-muted"
          on:click = { async() => {
            await assignDeUrl("Korea");
          }}>
          <CheckRegion checkFlag = { selDeUrl === 'Korea'}/>
          <span class="ml-2">{$i18n.t("Korea")}</span>
        </button>
        <!-- <button class="flex flex-row items-center w-full region-text-color my-2 select-none data-[highlighted]:bg-muted"
          on:click = { async () => {
            await assignDeUrl("Others");
          }}>
          <CheckRegion checkFlag = { selDeUrl === 'Others'}/>
          <span class="ml-2">{$i18n.t("Others")}</span>
        </button> -->
      <p class="region-text-color">{$i18n.t("When an access node is located in a specific region, it will by default preferentially connect to GPU computing nodes within the same region, reducing latency and enhancing performance.")}</p>
      </div>
      <div class="text-center mt-5 mb-2">
        <button class="primaryButton text-white rounded-lg px-3 py-2"
          on:click={ async() => await changeDeUrl() }>
          {$i18n.t("Save")}
        </button>
      </div>
    </div>
  </Modal>
</div>

<style>
  .region-fill-color {
    fill: rgba(184, 142, 86, 1);
  }
  .region-text-color {
    color: rgba(184, 142, 86, 1);
  }
</style>

