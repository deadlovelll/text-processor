package serial;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import shared.Producer;

public class SerialProducer {

    private final Producer messageProdcuer;

    public SerialProducer(Producer messageProducer)
    {
        this.messageProdcuer = messageProducer;
    }

    public void produce() throws
            IOException
    {
        String string = Files.readString(Path.of("src/main/java/data/data_100MB"));
        this.messageProdcuer.produceMessage(string);
    }
}
