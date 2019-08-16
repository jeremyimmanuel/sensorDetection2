package com.example.sensordetection;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.TextView;

import com.github.nkzawa.emitter.Emitter;
import com.github.nkzawa.socketio.client.IO;
import com.github.nkzawa.socketio.client.Socket;

public class ConnectPlayer extends AppCompatActivity {

    private Socket mSocket;
    Button startCollection;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT); //make it always portrait
        setContentView(R.layout.activity_connect_player);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        startCollection = findViewById(R.id.start_server_button);
        startCollection.setEnabled(false);

        SensorApplication app = (SensorApplication) getApplication();
        mSocket = app.getSocket();

        String deviceName = android.os.Build.MODEL;
        mSocket.emit("join player", deviceName);
        mSocket.emit("ask for button");

        mSocket.on("enable button", enableButton);
        mSocket.on("disable button", disableButton);
    }

    public void startProcess(View view){
        mSocket.emit("start collection");
        mSocket.on("start play", onPlay);
    }

    private void letsPlay() {
        mSocket.off("start play", onPlay);
        Intent playerIntent = new Intent(this, ActivatePlayer.class);
        startActivity(playerIntent);
    }

    private void enableStartButton(){
        startCollection.setEnabled(true);
    }

    private void disableStartButton(){
        startCollection.setEnabled(false);
    }

    private Emitter.Listener disableButton = new Emitter.Listener() {
        @Override
        public void call(final Object... args) {
            runOnUiThread(new Runnable() {
                @Override
                public void run(){
                    disableStartButton();
                }
            });
        }
    };

    private Emitter.Listener enableButton = new Emitter.Listener() {
        @Override
        public void call(final Object... args) {
            runOnUiThread(new Runnable() {
                @Override
                public void run(){
                    enableStartButton();
                }
            });
        }
    };

    private Emitter.Listener onPlay = new Emitter.Listener() {
        @Override
        public void call(final Object... args) {
            runOnUiThread(new Runnable() {
                @Override
                public void run(){
                    letsPlay();
                }
            });
        }
    };

    @Override
    protected void onDestroy() {
        super.onDestroy();
        mSocket.emit("leave player");
        mSocket.off("start play", onPlay);
        mSocket.off("enable button", enableButton);
        mSocket.off("disable button", disableButton);
    }


}
