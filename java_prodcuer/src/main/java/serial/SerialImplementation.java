package serial;

import java.io.IOException;
import java.net.URISyntaxException;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.concurrent.TimeoutException;

import shared.Producer;

public class SerialImplementation {

    private final SerialProducer serialMessageProducer;

    public SerialImplementation() throws
            IOException,
            URISyntaxException,
            NoSuchAlgorithmException,
            KeyManagementException,
            TimeoutException
    {
        Producer messageProducer = new Producer("content_parse2");
        this.serialMessageProducer = new SerialProducer(messageProducer);
    }

    public void run() throws
            IOException,
            TimeoutException
    {
        this.serialMessageProducer.produce();
    }
}
