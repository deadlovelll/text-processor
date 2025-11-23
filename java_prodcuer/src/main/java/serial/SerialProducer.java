package serial;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeoutException;
import java.util.UUID;

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
                "src/main/java/data/data_1MB",
        };
        int all = 1;
        UUID taskId = UUID.randomUUID();
        Map<String, Object> map = new HashMap<>();
        String content = Files.readString(Path.of("src/main/java/data/data_1MB"));
        map.put("taskId", taskId);
        map.put("all", all);
        map.put("value", content);
        this.messageProdcuer.produceMessage(map);
        this.messageProdcuer.closeConnection();
    }
}
