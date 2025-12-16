package com.degpt.app;

import android.os.Bundle;
import com.degpt.app.plugins.voicerecord.VoiceRecordPlugin;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        // 注册插件
        registerPlugin(VoiceRecordPlugin.class);
        super.onCreate(savedInstanceState);
    }

}
