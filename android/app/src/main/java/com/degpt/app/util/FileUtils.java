package com.degpt.app.util;


import android.content.Context;
import android.os.Environment;
import android.util.Log;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.text.SimpleDateFormat;
import java.util.Base64;
import java.util.Date;
import java.util.Locale;

public class FileUtils {

    /**
     * 将语音文件转换为Base64编码字符串（兼容API 23+）
     *
     * @param filePath 语音文件路径
     * @return Base64编码字符串
     * @throws IOException 当文件读取失败时抛出
     */
    public static String wavToBase64(String filePath) {

        String encodedString = "";
        try {
            File audioFile = new File(filePath);
            byte[] fileContent = Files.readAllBytes(audioFile.toPath());
            encodedString = Base64.getEncoder().encodeToString(fileContent);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return encodedString;
    }

    public static void saveStringToFile(String content, Context context) {
        try {
            // 保存到应用内部存储
            File storageDir = context.getExternalFilesDir(Environment.DIRECTORY_MUSIC);
            String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(new Date());
            String fileName = "degpt_" + timeStamp + ".txt";
            File file = new File(storageDir, fileName);
            FileWriter writer = new FileWriter(file);
            writer.write(content);
            writer.close();
            Log.d("SaveString", "文件保存成功：" + file.getAbsolutePath());
        } catch (IOException e) {
            Log.d("SaveString", "文件保存失败", e);
        }
    }

}
