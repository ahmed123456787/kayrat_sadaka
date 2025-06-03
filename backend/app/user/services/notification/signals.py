from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from core.models import Notification, CustomUser as User, Ressource


@receiver(post_save, sender=User)
def send_notification_on_activation(sender, instance, created, **kwargs):
    """Send a notification when a user is activated (after setting a password)."""

    if created:
        return  # Ignore new user creation, only track updates

    print("hello boy")
    try:
        print("active",instance.is_active) 
        if  instance.is_active:  
            mosque = instance.mosque
            message = f"{instance.first_name} {instance.last_name} has joined as a new member." 

            # Get all users belonging to the mosque
            users = User.objects.filter(mosque=mosque)
            notification = Notification.objects.create(message=message)  

            # Save notifications for each user
            for user in users:
                notification.users.add(user)  


            # Broadcast the notification to the WebSocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'mosque_{mosque}',
                {
                    'type': 'send_notification',
                    'message': message
                }
            )

    except User.DoesNotExist:
        pass 


@receiver(post_save, sender=Ressource)
def send_notification_ressource_empty(sender, instance, created, **kwargs):

    mosque = instance.distribution.responsible.mosque

    if instance.quantity == 0:
        users = User.objects.filter(mosque=mosque)
        message = f"The stock of {instance.ressource_type.name} is empty"
        notification = Notification.objects.create(message=message)

        for user in users: 
            notification.users.add(user)

        # Broadcast the notification to the WebSocket group
        channel_layer = get_channel_layer()
        print(f"Channel layer: {channel_layer}")
        async_to_sync(channel_layer.group_send)(
            f'mosque_{mosque.id}',
            {
                'type': 'send_notification',
                'message': message
            }
        )
        print("Notification sent to WebSocket group")