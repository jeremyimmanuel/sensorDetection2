package com.example.sensordetection;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

import com.github.nkzawa.socketio.client.IO;
import com.github.nkzawa.socketio.client.Socket;

import java.net.URISyntaxException;

public class MainActivity extends AppCompatActivity
{
    private Socket mSocket;
    private EditText urlInput;
    private Button connectButton;
    private Button playerRecorderButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT); //to make it start on portrait

        setContentView(R.layout.activity_main);

        //SensorApplication app = (SensorApplication) getApplication();
        //mSocket = app.getSocket();

        urlInput = (EditText) findViewById(R.id.insertURL);
        connectButton = (Button) findViewById(R.id.connectServerButton);
        playerRecorderButton = (Button) findViewById(R.id.playerRecorderButton);
        playerRecorderButton.setEnabled(false);

        if (android.os.Build.VERSION.SDK_INT > 9)
        {
            StrictMode.ThreadPolicy policy = new
                    StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }
    }

    public void connectServer(View view){
        String url = urlInput.getText().toString();
        System.out.println(url);
        SensorApplication app = (SensorApplication) getApplication();
        app.connectServer(url);
        mSocket = app.getSocket();
        mSocket.emit("hey waddup");

        connectButton.setEnabled(false);
        playerRecorderButton.setEnabled(true);

        //go to ChoosePlayerRecorder page
        //Intent playerIntent = new Intent(this, ChoosePlayerRecorder.class);
        //startActivity(playerIntent);
    }

    public void clearField(View v)
    {
        urlInput.setText("");
    }

    public void choosePlayerRecorder(View v)
    {
        Intent playerIntent = new Intent(this, ChoosePlayerRecorder.class);
        startActivity(playerIntent);
    }

}