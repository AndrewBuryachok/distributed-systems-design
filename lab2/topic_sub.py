import hazelcast

if __name__ == "__main__":
  client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        "127.0.0.1:5702",
        "127.0.0.1:5703",
    ],
  )
  my_topic = client.get_topic("my-distributed-topic").blocking()
  def on_message(message):
    print(f"Got message {message.message}")
  my_topic.add_listener(on_message)
  print("Listening for messages...")
  try:
    while True:
      pass
  except KeyboardInterrupt:
    print("Closing subscriber...")
    client.shutdown()
