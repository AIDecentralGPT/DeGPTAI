package com.degpt.app.plugins.aimanager;

import android.util.Log;

import java.io.File;
import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class HttpOpenAiManager {

    // 上次git临时修改配置文件读取
    private static String OPENAI_API_KEY= System.getenv("OPENAI_API_KEY");

    /**
     * 调用OpenAI API进行语音转录
     * @param audioFilePath 音频文件路径
     * @return 转录后的文本
     * @throws IOException 可能的IO异常
     */
    // 调用转录API
    public static void transcribeAudio(String audioFilePath) {
        File audioFile = new File(audioFilePath);
        if (!audioFile.exists()) {
            return;
        }
        // 构建请求体
        MultipartBody requestBody = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("file", audioFile.getName(),
                        RequestBody.create(audioFile, MediaType.parse("audio/mpeg")))
                .addFormDataPart("model", "gpt-audio")
                .build();

        // 构建请求
        Request request = new Request.Builder()
                .url("https://api.openai.com/v1/audio/transcriptions")
                .header("Authorization", "Bearer " + OPENAI_API_KEY)
                .post(requestBody)
                .build();

        // 发送异步请求（不能在主线程中进行网络请求）
        OkHttpClient client = new OkHttpClient();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.d("生成语音内容", e.toString());
                // 删除已创建的文件
                File file = new File(audioFilePath);
                if (file.exists()) {
                    file.delete();
                }
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful() && response.body() != null) {
                    String result = response.body().string();
                    Log.d("生成语音内容", result);
                } else {
                    String error = "错误代码: " + response.code() +
                            ", 信息: " + (response.body() != null ? response.body().string() : "无");
                    Log.d("生成语音内容", error);
                }
                File file = new File(audioFilePath);
                if (file.exists()) {
                    file.delete();
                }
            }
        });
    }

}
