import hazelcast

if __name__ == "__main__":
  client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        "127.0.0.1:5701",
    ],
  )
  my_topic = client.get_topic("my-distributed-topic").blocking()
  for i in range(100):
    my_topic.publish(i)
    print(f"Pub {i}")
  print("Finish")
  client.shutdown()
