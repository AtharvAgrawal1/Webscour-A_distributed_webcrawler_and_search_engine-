import pika


def publish_seed_url(seed_url):
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    
    channel.queue_declare(queue="webscour_queue", durable=True)

    
    channel.basic_publish(
        exchange="",
        routing_key="webscour_queue",
        body=seed_url,
        properties=pika.BasicProperties(
            delivery_mode=2,  
        ),
    )

    print(f"Published seed URL: {seed_url}")

    connection.close()


def main():
    seed_url = input("Enter seed URL: ").strip()
    publish_seed_url(seed_url)


if __name__ == "__main__":
    main()
