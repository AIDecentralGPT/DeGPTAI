import type { PermissionState } from '@capacitor/core';

// 权限状态枚举
export interface PermissionStatus {
  /**
   * Permission state for speechRecognition alias.
   *
   * On Android it requests/checks RECORD_AUDIO permission
   *
   * On iOS it requests/checks the speech recognition and microphone permissions.
   *
   * @since 5.0.0
   */
  audio: PermissionState;
}

export interface RealTimeSpeechPlugin {
  /**
   * 检查权限状态
   */
  checkPermissions(): Promise<PermissionStatus>;

  /**
   * 请求权限
   */
  requestPermissions(): Promise<PermissionStatus>;

  /**
   * 开始语音听写
   */
  startRecording(): Promise<void>;

  /**
   * 停止语音听写
   */
  stopRecording(): Promise<void>;

  /**
   * 释放语音听写
   */
  releaseRecording(): Promise<void>;

  // 监听音量变化
  addListener(
    eventName: 'volumeChange',
    listenerFunc: (data: { amplitude: number, db: number, level: number }) => void,
  ): Promise<PluginListenerHandle> & PluginListenerHandle;
  
  // 监听实时文本内容
  addListener(
    eventName: 'textChange',
    listenerFunc: (data: { text: string, content: string }) => void,
  ): Promise<PluginListenerHandle> & PluginListenerHandle;
}

export interface SpeechStatus {
  status: boolean;
  message: string;
}

export interface PluginListenerHandle {
  remove: () => Promise<void>;
}