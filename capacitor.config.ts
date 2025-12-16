import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.degpt.app',
  appName: 'DeGPT',
  webDir: 'build',
  plugins: {
    StatusBar: {
      overlaysWebView: false, // 禁用全屏覆盖
      style: 'dark', // 或 'light'
      backgroundColor: '#ffffff' // 设置背景色
    }
  }
};

export default config;
