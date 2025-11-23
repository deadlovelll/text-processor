package serial;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeoutException;
import java.util.UUID;
import java.util.Arrays;
import java.time.Instant;

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
            "data/data_1MB",
            "data/data_5MB",
            "data/data_10MB",
            "data/data_25MB",
            "data/data_50MB",
            "data/data_100MB",
        };
        for (String path : pathArray) {
            byte[] bytes = Files.readAllBytes(Path.of(path));
            int totalSize = bytes.length;
            int partSize = (int) Math.ceil(totalSize / 4.0);
            String startTime = Instant.now().toString();
            UUID taskId = UUID.randomUUID();

            for (int part = 0; part < 4; part++) {
                int start = part * partSize;
                int end = Math.min(start + partSize, totalSize);
                if (start >= end) break;
                byte[] chunk = Arrays.copyOfRange(bytes, start, end);
                Map<String, Object> message = new HashMap<>();
                message.put("taskId", taskId); 
                message.put("all", 4); 
                message.put("value", new String(chunk));
                message.put("start", startTime);
                this.messageProdcuer.produceMessage(message);
            }
        }
        this.messageProdcuer.closeConnection();
    }
}
