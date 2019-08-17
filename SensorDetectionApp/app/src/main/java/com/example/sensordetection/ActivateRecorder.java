package com.example.sensordetection;

import android.Manifest;
//import android.content.Context;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.widget.Toast;
//import android.view.View;
//import android.view.ViewGroup;
//import android.widget.Button;
//import android.widget.LinearLayout;
import com.github.nkzawa.emitter.Emitter;
import com.github.nkzawa.socketio.client.IO;
import com.github.nkzawa.socketio.client.Socket;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ActivateRecorder extends AppCompatActivity {

    private static final String LOG_TAG = "AudioRecordTest";
    private static String fileName = null;
    private MediaRecorder recorder = null;
    private Socket mSocket;
    private String timestamp;

    private MediaPlayer   player = null;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT); //make it always portrait
        setContentView(R.layout.activity_activate_recorder);

        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);


        SensorApplication app = (SensorApplication) getApplication();
        mSocket = app.getSocket();


        fileName = getExternalCacheDir().getAbsolutePath();
        timestamp = new SimpleDateFormat("yyyyMMddHHmmss'.3gp'").format(new Date());
        fileName += "/audiorecordtest_";
        fileName += timestamp;

        startRecording();

    }

    private void startRecording() {
        recorder = new MediaRecorder();
        recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        recorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        recorder.setOutputFile(fileName);
        recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);

        try {
            recorder.prepare();
        } catch (IOException e) {
            Log.e(LOG_TAG, "recorder prepare() failed");
        }

        recorder.start();
        mSocket.on("stop record", onRecStop);
    }

    private byte[] getBytes(File f)
            throws IOException
    {
        byte[] buffer = new byte [1024];
        ByteArrayOutputStream os = new ByteArrayOutputStream();
        FileInputStream fis = new FileInputStream(f);
        int read;
        while((read = fis.read(buffer)) != -1)
        {
            os.write(buffer, 0, read);
        }
        fis.close();
        os.close();
        return os.toByteArray();
    }

    private void stopRecording() {
        mSocket.off("stop record", onRecStop);

        if (recorder != null) {
            try {
                recorder.stop();
            } catch (RuntimeException stopException) {
//                recording_file.delete();
                recorder.reset();
                return;
            }

            recorder.release();
            recorder = null;

        }

        String deviceName = "" ;
        String fp = android.os.Build.FINGERPRINT;
        String[] fp_arr = fp.split("/");
        deviceName = fp_arr[4];
        deviceName = deviceName.substring(0, deviceName.indexOf(':'));
        deviceName += Build.MANUFACTURER;
        deviceName += "_" + timestamp;


        //convert file to bytearray
        try {
            File fileToSend = new File(fileName);
            byte[] byteArr = getBytes(fileToSend);
            mSocket.emit("Send File", byteArr, deviceName); //add another argument for recording name which should be the same name that's shown in main minus the brand name
        }
        catch (Exception e){
            Log.e(LOG_TAG, "No File Found");
        }
        Intent recorderIntent = new Intent(this, FinishRecording.class);
        startActivity(recorderIntent);
        finish();
    }

    private Emitter.Listener onRecStop = new Emitter.Listener() {
        @Override
        public void call(final Object... args) {
            runOnUiThread(new Runnable() {
                @Override
                public void run(){
                    stopRecording();
                }
            });

        }
    };


    @Override
    public void onStop() {
        super.onStop();
        if (recorder != null) {
            recorder.release();
            recorder = null;
        }

        if (player != null) {
            player.release();
            player = null;
        }

        mSocket.off("stop record", onRecStop);
    }


}
