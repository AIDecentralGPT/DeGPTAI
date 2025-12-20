// src/lib/utils/autoResumeGeneration.ts
import { browser } from '$app/environment';

type ResumeReason = 'init' | 'visibilitychange' | 'focus' | 'pageshow' | 'online' | 'timer-gap' | 'watchdog';

export type AutoResumeOptions = {
  // 读取当前“最后一条 assistant 消息”的状态
  getTarget: () => {
    // 是否是你要盯的那条（通常是最后一条 assistant）
    isTarget: boolean;
    // 生成是否已完成
    done: boolean;
    // 是否报错
    error: boolean;
    // 该消息是否在“应当继续生成”的状态（例如用户刚发问且还没 done）
    shouldContinue: boolean;
    // 最近一次内容变化时间（ms）
    lastUpdateAt: number;
    // 可选：用于重试的 parentId（一般是 user message id）
    parentId?: string;
  };

  // 继续生成（你的 continueGeneration）
  continueGeneration: () => Promise<void> | void;

  // 可选：如果 error 或 stalled 时你更想走“重连/重发”而不是 continue
  // force 参数由调用方决定是否使用（你现有 resentMessage 不接 force 也没关系）
  resentMessage?: (parentId?: string, force?: boolean) => Promise<void> | void;

  // 阈值：多久没增量就认为“卡住”
  stallMs?: number;

  // 轮询频率
  pollMs?: number;

  // 判定“从后台恢复”的时间 gap（移动端常见）
  gapThresholdMs?: number;

  debug?: boolean;
  logPrefix?: string;

  // 防抖：避免回来瞬间多次触发
  cooldownMs?: number;
};

export function installAutoResumeGeneration(opts: AutoResumeOptions): () => void {
  if (!browser) return () => {};

  const {
    getTarget,
    continueGeneration,
    resentMessage,
    stallMs = 8000,
    pollMs = 1000,
    gapThresholdMs = 2500,
    debug = true,
    logPrefix = '[auto-resume]',
    cooldownMs = 2000,
  } = opts;

  const log = (...args: any[]) => {
    if (!debug) return;
    // eslint-disable-next-line no-console
    console.log(logPrefix, ...args);
  };

  let lastFireAt = 0;
  const canFire = () => Date.now() - lastFireAt >= cooldownMs;

  const isOffline = () => {
    try {
      // navigator.onLine 在部分环境不可靠，但“false”时基本可信
      return typeof navigator !== 'undefined' && navigator.onLine === false;
    } catch {
      return false;
    }
  };

  const isHidden = () => {
    try {
      return typeof document !== 'undefined' && document.hidden === true;
    } catch {
      return false;
    }
  };

  const tryRecover = async (reason: ResumeReason) => {
    // 1) 离线直接跳过（避免反复触发无意义请求）
    if (isOffline()) {
      log('skip recover: offline', { reason });
      return;
    }

    // 2) 页面隐藏时跳过（避免后台/锁屏/切后台疯狂请求）
    //    visibilitychange / pageshow 由事件本身确保“回到前台”再触发
    if (isHidden() && reason !== 'visibilitychange' && reason !== 'pageshow') {
      log('skip recover: document hidden', { reason });
      return;
    }

    const t = getTarget();
    log('tryRecover', reason, t);

    if (!t.isTarget) return;
    if (!t.shouldContinue) return;

    // 3) error：允许 done=true 的错误态也能重试
    if (t.error && resentMessage && t.parentId && canFire()) {
      lastFireAt = Date.now();
      log('recover via resentMessage (error)', { reason, parentId: t.parentId });
      await resentMessage(t.parentId, true);
      return;
    }

    // 4) 已完成就不处理
    if (t.done) return;

    // 5) 卡住判定：超过 stallMs 没增量
    const stalled = Date.now() - t.lastUpdateAt >= stallMs;
    if (!stalled) return;

    if (!canFire()) return;
    lastFireAt = Date.now();

    // 6) stalled：优先走 resent（更稳，尤其是流断了/后台挂起）
    if (resentMessage && t.parentId) {
      log('recover via resentMessage (stalled)', {
        reason,
        parentId: t.parentId,
        stalledMs: Date.now() - t.lastUpdateAt,
      });
      await resentMessage(t.parentId, true);
      return;
    }

    // 7) 没有 resent 再走 continue
    log('recover via continueGeneration (stalled)', {
      reason,
      stalledMs: Date.now() - t.lastUpdateAt,
    });
    await continueGeneration();
  };

  // ---- 事件触发器（多挂一些成本低） ----
  const onVis = () => {
    log('event visibilitychange', { state: document.visibilityState, hidden: document.hidden });
    if (!document.hidden) void tryRecover('visibilitychange');
  };

  const onFocus = () => {
    log('event focus');
    void tryRecover('focus');
  };

  const onPageShow = (e: PageTransitionEvent) => {
    log('event pageshow', { persisted: e.persisted });
    void tryRecover('pageshow');
  };

  const onOnline = () => {
    log('event online');
    void tryRecover('online');
  };

  document.addEventListener('visibilitychange', onVis, { passive: true });
  window.addEventListener('focus', onFocus, { passive: true });
  window.addEventListener('pageshow', onPageShow, { passive: true });
  window.addEventListener('online', onOnline, { passive: true });

  // ---- timer gap：后台挂起/节流恢复时，经常只能靠它 ----
  let lastTick = Date.now();
  const timer = window.setInterval(() => {
    const now = Date.now();
    const gap = now - lastTick;
    lastTick = now;

    // gap 很大 => 曾被挂起/后台节流
    if (gap >= gapThresholdMs) {
      log('timer-gap detected', { gap });
      void tryRecover('timer-gap');
    } else {
      // 轻量 watchdog：如果已经很久没更新，也试一次（避免“永远不触发事件”的壳）
      void tryRecover('watchdog');
    }
  }, pollMs);

  log('installed', { stallMs, pollMs, gapThresholdMs, cooldownMs });

  // 初始化也跑一次（不做恢复也能打日志确认）
  void tryRecover('init');

  return () => {
    document.removeEventListener('visibilitychange', onVis);
    window.removeEventListener('focus', onFocus);
    window.removeEventListener('pageshow', onPageShow);
    window.removeEventListener('online', onOnline);
    window.clearInterval(timer);
    log('disposed');
  };
}
