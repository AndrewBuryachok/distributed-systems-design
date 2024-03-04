import hazelcast

if __name__ == "__main__":
  client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        "127.0.0.1:5701",
    ],
  )
  my_queue = client.get_queue("my-distributed-queue").blocking()
  for i in range(100):
    my_queue.put(i)
    print(f"Put {i}")
  my_queue.put(-1)
  print("Finish")
  client.shutdown()
