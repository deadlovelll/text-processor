package shared;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.net.URISyntaxException;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.Map;
import java.util.concurrent.TimeoutException;

public class Producer {

    private final String topicName;
    private final Channel channel;
    private final Connection conn;
    private final ObjectMapper mapper = new ObjectMapper();

    public Producer(String topicName) throws
            IOException,
            TimeoutException,
            URISyntaxException,
            NoSuchAlgorithmException,
            KeyManagementException
    {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setUri("amqp://guest:guest@localhost:5672");
        Connection conn = factory.newConnection();
        Channel channel = conn.createChannel();

        this.topicName = topicName;
        this.channel = channel;
        this.conn = conn;
    }

    public void produceMessage(Map<String, Object> message) throws
            IOException
    {
        channel.queueDeclare(topicName, true, false, false, null);
        byte[] messageBytes = mapper.writeValueAsBytes(message);
        channel.basicPublish("", topicName, null, messageBytes);
    }

    public void closeConnection() throws
            IOException,
            TimeoutException
    {
        channel.close();
        conn.close();
    }
}
