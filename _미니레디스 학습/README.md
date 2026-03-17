# 미니 레디스

[미니레디스 깃](https://github.com/tokio-rs/mini-redis)

- 생산에서 사용하지 말라(러닝 목적으로 만든 것)
- Tokio를 학습하기 위함

## Tokio Patterns

### 1. TCP Server

```
(server.rs)
```

### 2. Client Library

```
(client.rs)
```

### 3. State Shared across sockets

```

```

### 4. Framing

```
(connection.rs)
(frame.rs)
```

### 5. Graceful shutdown

```

```

### 6. Concurrent connection limiting

```
Semaphore : 다중 프로그래밍 운영체제에서 여러 프로세스가 데이터를 공유하면서 수행될 때 각 프로세스에서 공유 데이터를 접근(Access)하는 프로그램 코드 부분을 가리키는 말

공유 데이터를 여러 프로세스가 동시에 액세스하면 시간적인 차이 등으로 인해 잘못된 결과를 만들어 낼 수 있기 때문에 한 프로세스가 위험 부분을 수행하고 있을 때, 즉 공유 데이터를 액세스하고 있을 때는 다른 프로세스들은 절대로 그 데이터를 액세스하지 못하도록 막아야 함
```

### 7. Pub/Sub

```
광역폭 채널을 만들어 놓고
구독을 하는 방식
```

### 8. using a std::sync::Mutex in an async application

```
(db.rs)
```

### 9. Testing asynchronous code that relies on time

```

```
