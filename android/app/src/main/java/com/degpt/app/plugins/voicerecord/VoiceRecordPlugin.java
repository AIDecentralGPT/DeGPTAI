package com.degpt.app.plugins.voicerecord;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.pm.PackageManager;
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.os.Environment;
import android.util.Log;

import androidx.core.app.ActivityCompat;

import com.degpt.app.util.FileUtils;
import com.degpt.app.util.OkHttpSyncManager;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.annotation.Permission;
import com.getcapacitor.util.PermissionHelper;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ShortBuffer;
import java.nio.channels.FileChannel;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.concurrent.atomic.AtomicBoolean;

@CapacitorPlugin(
        name = "VoiceRecord",
        permissions = {
                @Permission(strings = {Manifest.permission.RECORD_AUDIO}, alias = "audio")
        }
)
public class VoiceRecordPlugin extends Plugin {

    private static final String TAG = "VoiceRecordPlugin";

    // 音频参数
    private static final int SAMPLE_RATE = 16000;
    private static final int CHANNEL_CONFIG = AudioFormat.CHANNEL_IN_MONO;
    private static final int AUDIO_FORMAT = AudioFormat.ENCODING_PCM_16BIT;
    private static final int BUFFER_SIZE = AudioRecord.getMinBufferSize(SAMPLE_RATE, CHANNEL_CONFIG, AUDIO_FORMAT);

    private AudioRecord audioRecord;
    private String outputFilePath;
    private FileOutputStream outputStream;
    private AtomicBoolean isRecording = new AtomicBoolean(false);

    private PluginCall allCall;

    // 开始录音
    @PluginMethod
    public void startRecording(PluginCall call) {
        // 检查权限
        String[] RECORD_PERMISSIONS = {
                Manifest.permission.RECORD_AUDIO
        };
        if (!PermissionHelper.hasPermissions(getContext(), RECORD_PERMISSIONS)) {
            call.reject("需要录音和存储权限");
            return;
        }

        try {
            // 创建输出文件
            File storageDir = getContext().getExternalFilesDir(Environment.DIRECTORY_MUSIC);
            String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(new Date());
            String fileName = "rec_" + timeStamp + ".wav";
            File outputFile = new File(storageDir, fileName);
            outputFilePath = outputFile.getAbsolutePath();

            // 初始化 AudioRecord
            if (ActivityCompat.checkSelfPermission(getContext(), Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                return;
            }



            audioRecord = new AudioRecord(
                    MediaRecorder.AudioSource.MIC,
                    SAMPLE_RATE,
                    CHANNEL_CONFIG,
                    AUDIO_FORMAT,
                    BUFFER_SIZE
            );

            if (audioRecord.getState() != AudioRecord.STATE_INITIALIZED) {
                call.reject("无法初始化录音设备");
                return;
            }

            // 创建输出流并写入 WAV 头
            outputStream = new FileOutputStream(outputFile);
            byte[] wavHeader = createWavHeader(0); // 初始数据长度为0
            outputStream.write(wavHeader);

            // 开始录音
            audioRecord.startRecording();
            isRecording.set(true);

            // 启动录音线程
            new Thread(new RecordingRunnable()).start();


            JSObject result = new JSObject();
            result.put("status", true);
            result.put("filePath", outputFilePath);
            call.resolve(result);

        } catch (Exception e) {
            Log.e(TAG, "录音启动失败", e);
            call.reject("录音启动失败: " + e.getMessage());
        }
    }

    // 录音线程
    private class RecordingRunnable implements Runnable {
        @Override
        public void run() {
            byte[] buffer = new byte[BUFFER_SIZE];
            try {
                while (isRecording.get() && audioRecord != null) {
                    int bytesRead = audioRecord.read(buffer, 0, buffer.length);
                    if (bytesRead > 0 && outputStream != null) {
                        outputStream.write(buffer, 0, bytesRead);
                    }
                    // 同步计算分贝
                    calculateAndSendVolume(buffer, bytesRead);
                }
            } catch (IOException e) {
                Log.e(TAG, "录音写入失败", e);
            } finally {
                stopRecordingInternal(allCall);
            }
        }
    }

    private byte[] createWavHeader(long totalAudioLen) {
        long totalDataLen = totalAudioLen + 36; // 数据长度 + 头信息长度
        long longSampleRate = SAMPLE_RATE;
        int channels = 1; // 单声道
        long byteRate = 16 * SAMPLE_RATE * channels / 8; // 字节率

        byte[] header = new byte[44];

        // RIFF/WAVE header
        header[0] = 'R'; header[1] = 'I'; header[2] = 'F'; header[3] = 'F';
        header[4] = (byte) (totalDataLen & 0xff);
        header[5] = (byte) ((totalDataLen >> 8) & 0xff);
        header[6] = (byte) ((totalDataLen >> 16) & 0xff);
        header[7] = (byte) ((totalDataLen >> 24) & 0xff);
        header[8] = 'W'; header[9] = 'A'; header[10] = 'V'; header[11] = 'E';

        // 'fmt ' chunk
        header[12] = 'f'; header[13] = 'm'; header[14] = 't'; header[15] = ' ';
        header[16] = 16; header[17] = 0; header[18] = 0; header[19] = 0; // Subchunk1Size
        header[20] = 1; header[21] = 0; // Audio format (1 = PCM)
        header[22] = (byte) channels; header[23] = 0; // Number of channels
        header[24] = (byte) (longSampleRate & 0xff);
        header[25] = (byte) ((longSampleRate >> 8) & 0xff);
        header[26] = (byte) ((longSampleRate >> 16) & 0xff);
        header[27] = (byte) ((longSampleRate >> 24) & 0xff);
        header[28] = (byte) (byteRate & 0xff);
        header[29] = (byte) ((byteRate >> 8) & 0xff);
        header[30] = (byte) ((byteRate >> 16) & 0xff);
        header[31] = (byte) ((byteRate >> 24) & 0xff);
        header[32] = (byte) (2 * 8 / 8); // Block align
        header[33] = 0;
        header[34] = 16; // Bits per sample
        header[35] = 0;

        // 'data' chunk
        header[36] = 'd'; header[37] = 'a'; header[38] = 't'; header[39] = 'a';
        header[40] = (byte) (totalAudioLen & 0xff);
        header[41] = (byte) ((totalAudioLen >> 8) & 0xff);
        header[42] = (byte) ((totalAudioLen >> 16) & 0xff);
        header[43] = (byte) ((totalAudioLen >> 24) & 0xff);

        return header;
    }

    private void updateWavHeader(String filePath) {
        try {
            File file = new File(filePath);
            long fileSize = file.length();
            long audioDataSize = fileSize - 44; // 减去WAV头的大小

            FileOutputStream fos = new FileOutputStream(filePath, true);
            fos.getChannel().position(0);
            fos.write(createWavHeader(audioDataSize));
            fos.close();

        } catch (Exception e) {
            Log.e(TAG, "UpdateWavHeader", e);
        }
    }

    // 取消录音
    @PluginMethod
    public void stopRecording(PluginCall call) {
        isRecording.set(false);
        allCall = call;
    }

    // 内部停止录音方法
    private void stopRecordingInternal(PluginCall call) {
        isRecording.set(false);
        if (audioRecord != null) {
            try {
                audioRecord.stop();
                audioRecord.release();
            } catch (Exception e) {
                Log.e(TAG, "停止录音设备失败", e);
            }
            audioRecord = null;
        }

        // 录制完成后更新WAV文件头
        updateWavHeader(outputFilePath);

        if (outputStream != null) {
            try {
                outputStream.close();
            } catch (IOException e) {
                Log.e(TAG, "关闭输出流失败", e);
            }
            outputStream = null;
        }

        File file = new File(outputFilePath);
        String base64 = FileUtils.wavToBase64(outputFilePath);

        // 删除文件
        if (outputFilePath != null) {
            if (file.exists()) {
                file.delete();
            }
        }

        JSObject result = new JSObject();
        result.put("status", true);
        result.put("filePath", base64);
        result.put("message", "录音取消");
        call.resolve(result);
    }

    /**
     * 复用音频数据计算分贝，避免多线程读取
     */
    @SuppressLint("DefaultLocale")
    private void calculateAndSendVolume(byte[] byteBuffer, int bytesRead) {
        if (bytesRead <= 0 || byteBuffer == null) return;

        // 1. 将byte数组转为short数组（16bit PCM数据）
        ShortBuffer shortBuffer = ByteBuffer.wrap(byteBuffer, 0, bytesRead)
                .order(java.nio.ByteOrder.LITTLE_ENDIAN) // 注意：PCM数据通常为小端序，需与硬件匹配
                .asShortBuffer();
        short[] shortBufferArr = new short[shortBuffer.remaining()];
        shortBuffer.get(shortBufferArr);

        // 2. 计算最大振幅（音量的原始值）
        int maxAmplitude = 0;
        for (short s : shortBufferArr) {
            int amplitude = Math.abs(s);
            if (amplitude > maxAmplitude) {
                maxAmplitude = amplitude;
            }
        }

        // 3. 计算分贝值（归一化到0-100范围，符合人类听觉感知）
        float db;
        if (maxAmplitude == 0) {
            db = 0;
        } else {
            // 参考值：16bit PCM的最大振幅为32767（2^15-1），计算分贝后归一化
            db = (float) (20 * Math.log10((double) maxAmplitude / 32767));
            db = Math.max(0, Math.min(100, db + 100)); // 映射到0-100
        }

        // 4. 转换为0-10的音量等级（方便前端显示）
        int volumeLevel = (int) (db / 10);

        // 5. 发送音量数据到前端
        JSObject volumeData = new JSObject();
        volumeData.put("amplitude", maxAmplitude);
        volumeData.put("db", String.format("%.1f", db)); // 保留1位小数
        volumeData.put("level", volumeLevel);
        notifyListeners("volumeChange", volumeData);
    }

}
