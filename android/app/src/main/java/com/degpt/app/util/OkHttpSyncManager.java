package com.degpt.app.util;

import okhttp3.*;
import java.io.IOException;
import java.util.Map;
import java.util.Set;

public class OkHttpSyncManager {
    private static OkHttpSyncManager instance;
    private OkHttpClient client;

    // 单例模式
    private OkHttpSyncManager() {
        client = new OkHttpClient.Builder()
                .connectTimeout(10, java.util.concurrent.TimeUnit.SECONDS)
                .readTimeout(10, java.util.concurrent.TimeUnit.SECONDS)
                .writeTimeout(10, java.util.concurrent.TimeUnit.SECONDS)
                .build();
    }

    public static synchronized OkHttpSyncManager getInstance() {
        if (instance == null) {
            instance = new OkHttpSyncManager();
        }
        return instance;
    }

    /**
     * 同步GET请求
     * @param url 请求地址
     * @return 响应结果字符串
     * @throws IOException 网络异常
     */
    public String syncGet(String url) throws IOException {
        Request request = new Request.Builder()
                .url(url)
                .get()
                .build();

        // 同步执行请求
        try (Response response = client.newCall(request).execute()) {
            if (response.isSuccessful() && response.body() != null) {
                return response.body().string();
            } else {
                throw new IOException("请求失败，状态码: " + response.code());
            }
        }
    }

    /**
     * 同步POST请求（表单提交）
     * @param url 请求地址
     * @param params 表单参数
     * @return 响应结果字符串
     * @throws IOException 网络异常
     */
    public String syncPost(String url, Map<String, String> params) throws IOException {
        // 构建表单参数
        FormBody.Builder formBuilder = new FormBody.Builder();
        if (params != null && !params.isEmpty()) {
            Set<Map.Entry<String, String>> entries = params.entrySet();
            for (Map.Entry<String, String> entry : entries) {
                formBuilder.add(entry.getKey(), entry.getValue());
            }
        }

        Request request = new Request.Builder()
                .url(url)
                .post(formBuilder.build())
                .build();

        // 同步执行请求
        try (Response response = client.newCall(request).execute()) {
            if (response.isSuccessful() && response.body() != null) {
                return response.body().string();
            } else {
                throw new IOException("请求失败，状态码: " + response.code());
            }
        }
    }
}