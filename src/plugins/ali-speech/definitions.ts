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

export interface AliSpeechPlugin {
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
  startListening(): Promise<void>;
  
  /**
   * 停止语音听写
   */
  stopListening(): Promise<void>;
  
}

export interface SpeechStatus {
  status: boolean;
  message: string;
}

export interface VolumeChange {
  volume: number;
}