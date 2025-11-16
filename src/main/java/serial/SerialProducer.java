package serial;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.concurrent.TimeoutException;

import com.rabbitmq.client.ShutdownSignalException;
import shared.Producer;

public class SerialProducer {

    private final Producer messageProdcuer;

    public SerialProducer(Producer messageProducer)
    {
        this.messageProdcuer = messageProducer;
    }

    public void produce() throws
            IOException,
            TimeoutException
    {
        String[] pathArray = {
                "src/main/java/data/data_100MB",
                "src/main/java/data/data_200MB",
                "src/main/java/data/data_500MB",
                "src/main/java/data/data_1GB",
        };
        for (String s : pathArray) {
            System.out.println("Producing " + s);
            String content = new String(Files.readAllBytes(Path.of(s)));
            this.messageProdcuer.produceMessage(content);
        }
        this.messageProdcuer.closeConnection();
    }
}
