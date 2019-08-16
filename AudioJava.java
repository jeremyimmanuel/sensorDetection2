//package fileWrite;

import java.io.*;
import java.nio.file.Files;


public class AudioJava 
{
    public static void main(String[] args)
    {
        try {
            File f = new File("bear_growl_y.wav");
            byte[] bytesFromFile = getBytes(f);


            File destination = new File("new_file.wav");
            Files.write(destination.toPath(), bytesFromFile);
        } catch (Exception e) {
            //TODO: handle exception
        }

        
    }

    public static byte[] getBytes(File f)
    throws FileNotFoundException, IOException
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

    public static void toFile(byte[] data, File destination)
    {
        try(FileOutputStream fos = new FileOutputStream(destination)){
            fos.write(data);
            fos.close();
        }
        catch(Exception e){
            System.out.println("error!");
        }

    }
}