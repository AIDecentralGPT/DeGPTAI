<script lang="ts">
  import { getContext } from 'svelte';
  import { getModels as _getModels, checkUniapp, checkPlatform } from '$lib/utils';
  import Icon from '@iconify/svelte';
  import {
    user,
    chats,
    showRewardsHistoryModal,
    showRewardDetailModal,
    downLoadUrl,
    showDownLoad,
    mobile,
    settings,
    models,
    showSidebar,
    showWalletView,
    showNewWalletModal,
    showShareModal,
    showUserVerifyModal,
    binanceFlag,
  } from '$lib/stores';

  import { getRewardsCount, clockIn } from '$lib/apis/rewards/index.js';

  import DownLoadModal from '$lib/components/download/DownLoadModal.svelte';
  import { RewardProperties } from '$lib/constants';
  import { toast } from 'svelte-sonner';

  const i18n = getContext('i18n');

  let clockLoading = false;

  // 优化：使用 Iconify 图标名称代替冗长的 SVG 字符串，风格与上方保持一致
  let items = [
    {
      id: 'new_wallet',
      text: 'Create Wallet',
      reward: RewardProperties?.regist + ' DGC',
      icon: 'lucide:wallet', // 统一使用钱包图标
    },
    {
      id: 'clock_in',
      text: 'Clock In',
      reward: RewardProperties?.clockinall + ' DGC',
      icon: 'lucide:calendar-check', // 统一使用日历打卡图标
    },
    {
      id: 'invite',
      text: 'Share',
      reward: RewardProperties?.invite + ' DGC',
      icon: 'lucide:share-2', // 统一使用分享图标
    },
    // {
    //   id: 4,
    //   text: "Make First Transaction",
    //   reward: "3000DGCs",
    //   icon: ''
    // }
  ];

  let rewardsCount: any = {};

  async function getCount() {
    if ($user) {
      const res = await getRewardsCount(localStorage.token);
      if (res) {
        Object.keys(res).forEach((key) => {
          if (res[key]) {
            rewardsCount[key] = res[key].length;
          } else {
            rewardsCount[key] = 0;
          }
        });
        console.log('rewardsCount', rewardsCount);
      }
    }
  }

  $: if ($user?.id?.startsWith('0x')) {
    getCount();
  }

  let modObj: any = [];
  $: {
    let selmodels = $settings?.models ?? ['qwen3-max-preview'];
    if (selmodels.length > 0) {
      modObj = $models.filter((item) => selmodels.includes(item?.model));
    }
    if (modObj.length == 0) {
      modObj = [$models.find((item) => item?.model === 'qwen3-max-preview')];
    }
  }

  // ... 你原本的 import 代码 ...

  // 1. 定义按钮的基础数据配置
  const downloadOptions = {
    ios: {
      icon: 'mdi:apple',
      text: 'App Store',
      url: 'https://apps.apple.com/us/app/degpt/id6504377109?platform=iphone',
      // iOS 图标 hover 变黑/白
      hoverClass: 'group-hover:text-black dark:group-hover:text-white',
    },
    google: {
      icon: 'mdi:google-play',
      text: 'Google Play',
      url: 'https://play.google.com/store/apps/details?id=com.degpt.app',
      // Google 图标 hover 变青色
      hoverClass: 'group-hover:text-[#00C4B3]',
    },
    apk: {
      icon: 'mdi:android',
      text: 'APK',
      url: '/static/app/degpt_v2.0250928.apk',
      // Android 图标 hover 变绿色
      hoverClass: 'group-hover:text-[#3DDC84]',
    },
  };

  // 2. 根据平台逻辑，计算当前需要显示的按钮数组
  // 使用 reactive 声明 ($:) 确保 checkPlatform 变化时（虽然通常不变）能正确响应
  $: activeDownloadButtons = (() => {
    const platform = checkPlatform();
    if (platform === 'ios') {
      return [downloadOptions.ios];
    } else if (platform === 'android') {
      return [downloadOptions.google, downloadOptions.apk];
    } else {
      // 默认/PC端：显示 Google Play -> APK -> App Store (保留你之前的顺序)
      return [downloadOptions.google, downloadOptions.apk, downloadOptions.ios];
    }
  })();

  // ... 其他 import ...

  // 1. 定义按钮的数据配置
  // 使用 $: 声明，确保当 $user, $binanceFlag, $i18n 变化时，按钮状态自动更新
  $: actionButtons = [
    {
      id: 'website',
      icon: 'lucide:globe',
      // 这里可以拼接翻译文本
      label: `${$i18n.t('Visit')}${$i18n.t('official website')}`,
      show: true, // 始终显示
      variant: 'default', // 默认灰色样式
      action: () => {
        if (checkUniapp()) {
          $downLoadUrl = 'https://www.decentralgpt.org';
          $showDownLoad = true;
        } else {
          window.open('https://www.decentralgpt.org', '_blank');
        }
      },
    },
    {
      id: 'history',
      icon: 'lucide:history',
      label: $i18n.t('Rewards History'),
      // 显示条件：不是币安且用户ID以0x开头
      show: !$binanceFlag && $user?.id?.startsWith('0x'),
      variant: 'default',
      action: () => {
        $showRewardsHistoryModal = true;
      },
    },
    {
      id: 'details',
      icon: 'lucide:scroll-text',
      label: $i18n.t('Rewards Details'),
      // 显示条件：不是币安
      show: !$binanceFlag,
      variant: 'default',
      action: () => {
        $showRewardDetailModal = true;
      },
    },
    {
      id: 'wallet',
      icon: 'lucide:wallet',
      label: $i18n.t('Enter wallet'),
      show: true, // 始终显示
      variant: 'amber', // 特殊琥珀色样式
      action: () => {
        $showSidebar = true;
        $showWalletView = true;
      },
    },
  ];
</script>

<div>
  <!-- 模型介绍 -->
  {#if modObj}
    <div class="flex flex-col items-center w-full space-y-1.5 text-center">
      <div class="relative flex items-center justify-center">
        <div class="absolute inset-0 bg-blue-500/20 blur-xl rounded-full" />
        <img
          class="relative w-10 h-10 md:w-12 md:h-12 rounded-xl border border-white/10"
          src={modObj[0]?.modelicon}
          alt=""
        />
      </div>

      <span class="text-xl font-bold">{modObj[0]?.name}</span>

      <div class="px-4 py-1 rounded-full bg-white/5 border border-white/5">
        <span class="text-sm text-gray-500 dark:text-gray-300">
          {$i18n.t(modObj[0]?.desc)}
        </span>
      </div>
    </div>
  {/if}
  <div class="flex my-2">
    <!-- 节点选择 -->
    <!-- <div class="flex flex-col {$mobile ? '' : 'pb-6'}">
      <ModelDeSelector />
      //<span class="text-xl ml-10 mt-1">
      //  {$i18n.t("Unlimited DGC Reward Task")}
      //</span>
    </div> -->
    <div class="grid grid-cols-1 md:grid-cols-2 w-full gap-4">
      <!-- 下载按钮组 -->
      <div class="w-full flex order-1 md:order-1 md:justify-start">
        {#if !checkUniapp()}
          <div class="flex flex-wrap gap-2 justify-center md:justify-start items-center">
            {#each activeDownloadButtons as btn}
              <button
                class="group flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-gray-200 dark:border-white/10 bg-white dark:bg-[#1a1a1a] active:bg-gray-100 dark:active:bg-[#252525] active:scale-95 transition-all duration-200 hover:bg-gray-100 dark:hover:bg-[#252525]"
                on:click={() => {
                  window.open(btn.url, '_blank');
                }}
              >
                <Icon
                  icon={btn.icon}
                  class="w-3.5 h-3.5 text-gray-500 dark:text-gray-400 {btn.hoverClass} transition-colors"
                />
                <span
                  class="text-xs font-medium text-gray-500 dark:text-gray-400 group-hover:text-black dark:group-hover:text-white"
                >
                  {btn.text}
                </span>
              </button>
            {/each}
          </div>
        {/if}
      </div>

      <!-- 官网按钮组 -->
      <div class="flex flex-wrap gap-2 w-full md:justify-end order-1 md:order-2">
        {#each actionButtons as btn (btn.id)}
          {#if btn.show}
            <button
              class="group flex items-center gap-1.5 p-2 rounded-full transition-all duration-200 active:scale-95 shadow-sm dark:shadow-none border
                {btn.variant === 'amber'
                ? ' bg-primary border-none'
                : 'border-gray-200 dark:border-white/10 bg-white dark:bg-[#1a1a1a] active:bg-gray-100 dark:active:bg-[#252525]'}"
              on:click={btn.action}
            >
              <Icon
                icon={btn.icon}
                class="w-3 md:w-4 h-3 md:h-4 transition-colors 
                  {btn.variant === 'amber'
                  ? 'text-gray-100 dark:text-gray-300'
                  : 'text-gray-400 group-hover:text-amber-500'}"
              />

              <span
                class="text-xs md:text-sm
                  {btn.variant === 'amber'
                  ? 'text-gray-100 dark:text-gray-300'
                  : ' text-gray-500 dark:text-gray-300 group-hover:text-black dark:group-hover:text-white'}"
              >
                {btn.label}
              </span>
            </button>
          {/if}
        {/each}
      </div>
    </div>
  </div>
  {#if !$binanceFlag}
    <div class="flex flex-wrap lg:flex-nowrap gap-3 w-full my-3">
      {#each items as item, index}
        {#if (item.id !== 'new_wallet' && $user?.id?.startsWith('0x')) || (item.id === 'new_wallet' && !$user?.id?.startsWith('0x'))}
          <div
            class="flex items-center justify-between w-full lg:w-1/3 p-2 rounded-xl border-gray-200 dark:border-white/10 shadow-sm dark:shadow-none group gap-1.5 transition-all duration-200 active:scale-95 border
             border-amber-500/30 dark:bg-amber-500/10 active:bg-amber-100 dark:active:bg-amber-500/20"
          >
            <div class="flex flex-col gap-1.5">
              <div
                class="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-gray-500 dark:text-gray-400"
              >
                <Icon icon={item.icon} class="w-3.5 h-3.5" />
                <span>{$i18n.t(item.text)}</span>
              </div>

              <span class="text-base font-black text-primary leading-none">
                {item.reward}
              </span>
            </div>

            <button
              disabled={clockLoading && item.id === 'clock_in'}
              class=" flex items-center text-gray-100 dark:text-gray-300 gap-1.5 py-1 px-2 text-[13.5px] rounded-full transition-all duration-200 active:scale-95 border
             border-amber-500/30 bg-primary dark:bg-amber-500/10"
              on:click={async () => {
                // --- 逻辑代码完整保留 ---
                if (item.id === 'new_wallet') {
                  $showNewWalletModal = true;
                } else if (item.id === 'invite') {
                  $showShareModal = true;
                } else if (item.id === 'clock_in') {
                  if (!$user?.verified) {
                    toast.warning($i18n.t('To claim the reward, you must first complete user verification !'));
                    $showUserVerifyModal = true;
                  } else if ($chats.length > 0) {
                    clockLoading = true;
                    await clockIn(localStorage.token)
                      .then((res) => {
                        console.log('Clock In  res', res);
                        getCount();
                        if (res?.ok) {
                          toast.success($i18n.t(res?.message, RewardProperties));
                        }
                        if (res?.detail) {
                          toast.warning($i18n.t(res?.detail, RewardProperties));
                        }
                      })
                      .catch((res) => {
                        console.log('Clock In  error', res);
                      });
                    clockLoading = false;
                  } else {
                    toast.warning($i18n.t('You need to complete a conversation to receive a reward ！'));
                  }
                }
                return;
              }}
            >
              {(($user?.id?.startsWith('0x') && rewardsCount[item.id]) || 0) > 0
                ? clockLoading && item.id === 'clock_in'
                  ? $i18n.t('Done...')
                  : $i18n.t('Done')
                : clockLoading && item.id === 'clock_in'
                ? $i18n.t('Get Now...')
                : $i18n.t('Get Now!')}
            </button>
          </div>
        {/if}
      {/each}
    </div>
  {/if}
</div>

<DownLoadModal bind:show={$showDownLoad} />

<style>
  .mt-20 {
    margin-top: 20px;
  }
  .mr-10 {
    margin-right: 10px;
  }
  .direction-column {
    flex-direction: column;
  }
  .region-text-color {
    color: rgba(184, 142, 86, 1);
  }
</style>
