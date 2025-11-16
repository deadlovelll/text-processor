import serial.SerialImplementation;

import java.io.IOException;
import java.net.URISyntaxException;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.concurrent.TimeoutException;

public class Main {
    public static void main(String[] args) throws
            IOException,
            URISyntaxException,
            NoSuchAlgorithmException,
            KeyManagementException,
            TimeoutException
    {
        SerialImplementation serial = new SerialImplementation();
        serial.run();
    }
}
