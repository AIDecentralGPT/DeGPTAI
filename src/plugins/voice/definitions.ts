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

export interface VoicePlugin {
  /**
   * 检查权限状态
   */
  checkPermissions(): Promise<PermissionStatus>;
  
  /**
   * 请求权限
   */
  requestPermissions(): Promise<PermissionStatus>;
  
  /**
   * 开始录音
   */
  startRecording(): Promise<void>;

  /**
   * 停止录音
   */
  stopRecording(): Promise<VoiceStatus>;

  // 监听音量变化
  addListener(
    eventName: 'volumeChange',
    listenerFunc: (data: { amplitude: number, db: number, level: number }) => void,
  ): Promise<PluginListenerHandle> & PluginListenerHandle;
  
}

export interface VoiceStatus {
  status: boolean;
  filePath: string;
  message: string;
}

export interface VolumeChange {
  volume: number;
}

export interface PluginListenerHandle {
  remove: () => Promise<void>;
}