package com.degpt.app;

import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;

import androidx.core.content.ContextCompat;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 设置状态栏颜色
        initSamsung();
    }

    // 设置状态栏颜色
    private void initSamsung() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
            window.setStatusBarColor(ContextCompat.getColor(this, com.getcapacitor.android.R.color.colorBlack));

            // 针对三星手机的特殊处理
            if (isSamsungDevice()) {
                fixSamsungStatusBar(window);
            }
        }
    }

    // 判断是否为三星设备
    private boolean isSamsungDevice() {
        return "samsung".equalsIgnoreCase(Build.MANUFACTURER);
    }

    // 三星手机状态栏修复方法
    private void fixSamsungStatusBar(Window window) {
        try {
            // 尝试清除可能影响状态栏的标志
            window.clearFlags(0x04000000); // WindowManager.LayoutParams.FLAG_TRANSLUCENT_STATUS

            // 如果是One UI系统，尝试设置特定标志
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                window.getAttributes().layoutInDisplayCutoutMode =
                        WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
            }

            // 强制重绘状态栏
            window.getDecorView().setSystemUiVisibility(
                    View.SYSTEM_UI_FLAG_LAYOUT_STABLE |
                            View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
