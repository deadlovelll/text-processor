package shared;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DeliverCallback;

import java.io.IOException;
import java.net.URISyntaxException;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.concurrent.TimeoutException;

public class Consumer {

    private final String topicName;
    private final Channel channel;

    public Consumer(String topicName) throws
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
    }

    public void consumeMessages() throws
            IOException
    {
        channel.exchangeDeclare(topicName, "fanout");
        String queueName = channel.queueDeclare().getQueue();
        channel.queueBind(queueName, topicName, "");
        System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

        DeliverCallback deliverCallback = (consumerTag, delivery) -> {
            String message = new String(delivery.getBody(), "UTF-8");
            System.out.println(" [x] Received '" + message + "'");
        };
        channel.basicConsume(queueName, true, deliverCallback, consumerTag -> {});
    }
}
