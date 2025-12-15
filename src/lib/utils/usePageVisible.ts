// $lib/utils/usePageVisible.ts
import { onMount, onDestroy } from 'svelte';

export function usePageVisible(callback: () => void) {
  const handleVisibilityChange = () => {
    // 步骤 2：先确认事件本身有没有触发（不管此时是隐藏还是显示）
    console.log('👀 [Hook] 监听到 visibilitychange 事件！当前状态:', document.visibilityState);

    // 步骤 3：确认是否满足“可见”条件
    if (!document.hidden) {
      console.log('✅ [Hook] 页面变回可见状态，准备执行 callback()...');

      if (typeof callback === 'function') {
        callback();
      } else {
        console.error('❌ [Hook] 传入的 callback 不是一个函数！', callback);
      }
    } else {
      console.log('⏸️ [Hook] 页面变为隐藏，不执行 callback');
    }
  };

  onMount(() => {
    // 步骤 1：确认挂载成功
    console.log('🪝 [Hook] usePageVisible 已挂载，正在监听 document 事件...');
    document.addEventListener('visibilitychange', handleVisibilityChange);
  });

  // onDestroy(() => {
  //   console.log('🗑️ [Hook] usePageVisible 已销毁，移除监听器');
  //   if (typeof document !== 'undefined') {
  //     document.removeEventListener('visibilitychange', handleVisibilityChange);
  //   }
  // });
}
