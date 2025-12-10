package com.degpt.app.util;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.Network;
import android.net.NetworkCapabilities;
import android.os.Build;

/**
 * 网络工具类：判断设备是否有可用网络连接
 */
public class NetworkUtils {

    /**
     * 判断设备是否有网络连接（包括移动数据、WiFi等）
     * @param context 上下文
     * @return true：有网络连接；false：无网络连接
     */
    public static boolean isNetworkAvailable(Context context) {
        // 获取连接管理器
        ConnectivityManager connectivityManager =
                (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);

        if (connectivityManager == null) {
            return false; // 设备不支持网络管理，视为无网络
        }

        // 适配 Android 10 及以上版本
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            // 获取当前活跃网络
            Network activeNetwork = connectivityManager.getActiveNetwork();
            if (activeNetwork == null) {
                return false; // 无活跃网络
            }

            // 获取网络能力
            NetworkCapabilities networkCapabilities =
                    connectivityManager.getNetworkCapabilities(activeNetwork);

            if (networkCapabilities == null) {
                return false;
            }

            // 检查是否有可用的网络传输方式（移动数据、WiFi、以太网等）
            return networkCapabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR)
                    || networkCapabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)
                    || networkCapabilities.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET)
                    || networkCapabilities.hasTransport(NetworkCapabilities.TRANSPORT_BLUETOOTH)
                    || networkCapabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI_AWARE);
        } else {
            // 适配 Android 6.0 以下版本（已废弃的API，但仍可工作）
            android.net.NetworkInfo networkInfo = connectivityManager.getActiveNetworkInfo();
            // 网络信息不为空且已连接
            return networkInfo != null && networkInfo.isConnected();
        }
    }

    /**
     * 判断是否为WiFi连接
     * @param context 上下文
     * @return true：当前是WiFi连接；false：不是WiFi连接
     */
    public static boolean isWifiConnected(Context context) {
        ConnectivityManager connectivityManager =
                (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);

        if (connectivityManager == null) {
            return false;
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            Network activeNetwork = connectivityManager.getActiveNetwork();
            if (activeNetwork == null) {
                return false;
            }

            NetworkCapabilities networkCapabilities =
                    connectivityManager.getNetworkCapabilities(activeNetwork);

            return networkCapabilities != null
                    && networkCapabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI);
        } else {
            android.net.NetworkInfo networkInfo =
                    connectivityManager.getNetworkInfo(ConnectivityManager.TYPE_WIFI);
            return networkInfo != null && networkInfo.isConnected();
        }
    }

    /**
     * 判断是否为移动数据连接
     * @param context 上下文
     * @return true：当前是移动数据连接；false：不是移动数据连接
     */
    public static boolean isMobileDataConnected(Context context) {
        ConnectivityManager connectivityManager =
                (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);

        if (connectivityManager == null) {
            return false;
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            Network activeNetwork = connectivityManager.getActiveNetwork();
            if (activeNetwork == null) {
                return false;
            }

            NetworkCapabilities networkCapabilities =
                    connectivityManager.getNetworkCapabilities(activeNetwork);

            return networkCapabilities != null
                    && networkCapabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR);
        } else {
            android.net.NetworkInfo networkInfo =
                    connectivityManager.getNetworkInfo(ConnectivityManager.TYPE_MOBILE);
            return networkInfo != null && networkInfo.isConnected();
        }
    }
}