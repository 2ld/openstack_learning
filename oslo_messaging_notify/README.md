## Oslo messaging

Oslo messaging提供了两个独立的API：
1. oslo.messaging.rpc，实现了客户端-服务器远程过程调用；
2. oslo.messaging.notify，推送和处理事件通知。

接下来介绍oslo messaging中的几个重要的概念。 
### Transport
Transport：处理消息发送的抽象层。
RPC创建`transport`方式：
```
def get_rpc_transport(conf, url=None,
                      allowed_remote_exmods=None)
```
但是经验证以后，该方法不存在，所以RPC创建`transport`时，还是使用`get_transport`方法即可。

notify创建`transport`方式:
```
def get_notification_transport(conf, url=None,
                               allowed_remote_exmods=None)
```
如果创建时不提供URL，会默认采用配置文件中`notifications`部分的`URL`值，如果该值没有指定，会使用`default`部分的`transport_url`的值。

### Target
Target：消息目的地的标识。
`Target`封装了所有信息，以确定消息应该发送到哪里或服务器正在监听哪些消息。

声明方式：
```
class oslo_messaging.Target(exchange=None, topic=None, namespace=None, version=None, server=None, fanout=None, legacy_namespaces=None)
```
部分参数介绍：
`topic`: String类型，服务端暴露出的**一组**接口的名称的标识。多个服务器可以监听一个`topic`，消息将被分派到以轮询方式选择的服务器之一（`fanout`设置为`True`时例外）。

`exchange`: String类型，`topic`的作用域。

`namespace`: String类型，服务端暴露出的一组特定RPC接口（方法）的标识。默认接口（方法）是没有命名空间的，被称为空命名空间。

`version`: 略。

`server`: String类型，RPC客户端可以请求将消息定向到特定服务器，而不仅仅是监听该`topic`的服务器池中的一个。

`fanout`: 客户端可能会要求将消息的副本传递给所有监听该`topic`的server，而不仅仅是其中的一个server，此时将
`fanout`设置为`True`即可。

封装在Target对象中的信息与所调用的API的有关，介绍几中API：
```
an RPC Server’s target:topic and server is required; exchange is optional
an RPC endpoint’s target: namespace and version is optional
an RPC client sending a message: topic is required, all other attributes optional
a Notification Server’s target: topic is required, exchange is optional; all other attributes ignored
a Notifier’s target: topic is required, exchange is optional; all other attributes ignored
```

### Executors

`Executors`控制着接收到消息后如何调度正在运行的服务执行。这种调度可以是同步的或是异步的。

同步的`executor`将会在`Server`进程上执行。也即是说，在同一时间内，一个`Server`只能处理一个消息。其它后续到来的消息将不会被立即执行，直到当前消息处理完毕。例如：在RPCServer的情况下，一次只会调用一个方法调用。同步的`executor`保证了消息执行的完整性、顺序性（消息被接受的顺序）。

异步的`executor`将同时处理接收到的消息。服务器线程不会被消息处理阻塞，并且还可以继续为传入的消息提供服务。没有顺序保证，消息处理可能会以与收到的不同的顺序完成。`executor`可配置限制一次处理的最大消息数。

### 几种可用的executor
#### blocking

一种同步的`executor`，为默认值。
#### eventlet
异步`executor`,并且使用绿色的线程池去异步的处理消息。

#### threading
异步`executor`,使用线程池去异步的处理消息。

### RPC

#### RPC Server
RPC Server暴露了一组`endpoint`，每个`endpoint`中有多个方法，这些方法可以被远程的`Client`调用，前提是该`Client`制定了正确的`transport`。

创建RPC Server，需要提供一个`transport`，一个`Target`和一组`endpoint`。
创建方式如下：
```
get_rpc_server(transport, target, endpoints,
                        executor='blocking', serializer=None, access_policy=None)
```
Note：
1. 如果`exetutor`使用`eventlet`,则线程和时间库需要进行monkepatched(`eventlet.monkey_patch()`)。
2. 如果多个`endpoint`中声明了相同的方法，以`endpoints`中指定的顺序为准。（已验证）

#### RPC Client
RPC Clinet：远程调用`RPC Server`的方法。
RPCClient类负责通过消息传输向远程RPC服务器发送方法调用和接收返回值。
创建方式如下：
```
oslo_messaging.RPCClient(transport, target, timeout=None, version_cap=None, serializer=None, retry=None)
```
支持两种方式：RPC calls and RPC casts.
RPC calls：同步调用，通常情况下，同步调用`server`端的方法，该方法都会有一个返回值。
RPC casts：异步调用，调用的`server`端的方法是没有返回值的。

### notify
对于notify我们重点关注它是如何监听消息的。
创建notify的listener时，需要提供一个`transport`，一个`Target`和一组`endpoint`。
创建方式如下：
```
oslo_messaging.get_notification_listener(transport, targets, endpoints, executor='blocking', serializer=None, allow_requeue=False, pool=None)
```
其中，`transport`,`targets`,`endpoints`,`executor`的上边已经介绍过，不在赘述，需要注意的是`allow_requeue`参数，是否需要支持NotificationResult.REQUEUE，即如果`allow_requeue`设置为`True`时，允许消息重复发送，反之则不行。
参考链接：
1. [RabbitMQ and Oslo.messaging](http://www.openstack.cn/?p=3514)
2. [Openstack 官网](https://docs.openstack.org/oslo.messaging/latest/reference/index.html)