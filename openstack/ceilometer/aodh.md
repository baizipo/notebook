# Aodh

Aodh把告警和事件分开处理，使告警的检测和响应更加及时。

## 后端服务

1. aodh-api. 为告警数据的存储和访问提供借口。
2. aodh-evaluator. 根据统计的数据，来评估是否需要触发告警.
3. aodh-listener. 监听事件，触发事件相关的告警.
4. aodh-notifier. 根据配置的告警方式，发出告警.

