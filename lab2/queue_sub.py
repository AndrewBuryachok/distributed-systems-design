import hazelcast

if __name__ == "__main__":
  client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        "127.0.0.1:5702",
        "127.0.0.1:5703",
    ],
  )
  my_queue = client.get_queue("my-distributed-queue").blocking()
  while True:
    i = my_queue.take()
    print(f"Take {i}")
    if (i == -1):
      break
  my_queue.put(-1)
  print("Finish")
  client.shutdown()
