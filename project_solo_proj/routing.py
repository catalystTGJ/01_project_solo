from channels.routing import ChannelNameRouter, ProtocolTypeRouter
from tasks.consumers import BackgroundTaskConsumer

application = ProtocolTypeRouter({
    'channel': ChannelNameRouter({
        'background-tasks': BackgroundTaskConsumer,
    })
})