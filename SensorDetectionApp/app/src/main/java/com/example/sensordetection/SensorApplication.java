package com.example.sensordetection;

import android.app.Application;
import com.github.nkzawa.socketio.client.IO;
import com.github.nkzawa.socketio.client.Socket;
import java.net.URISyntaxException;

public class SensorApplication extends Application {
    private Socket mSocket;


    public void connectServer(String url)
    {
        try
        {
            mSocket = IO.socket(url);   //old: (Constants.SERVER_URL);
        }
        catch (URISyntaxException e)
        {
            throw new RuntimeException(e);
        }
        mSocket.connect();
    }

    public Socket getSocket() {
        return mSocket;
    }
}
