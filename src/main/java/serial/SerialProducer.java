package serial;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.concurrent.TimeoutException;

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
//        String[] pathArray = {
//                "src/main/java/data/data_100MB",
//                "src/main/java/data/data_200MB",
//                "src/main/java/data/data_500MB",
//                "src/main/java/data/data_1GB",
//                "src/main/java/data/data_1p5_GB"
//        };
//        for (String path : pathArray) {
//            String content = new String(Files.readAllBytes(Path.of(path)));
//            this.messageProdcuer.produceMessage(content);
//        }
        String content = "content";
        this.messageProdcuer.produceMessage(content);
        this.messageProdcuer.closeConnection();
    }
}
