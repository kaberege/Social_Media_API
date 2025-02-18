from rest_framework import serializers
from notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.PrimaryKeyRelatedField(read_only=True)  # recipient is a foreign key
    actor = serializers.PrimaryKeyRelatedField(read_only=True)  # actor is a foreign key
    target = serializers.SerializerMethodField()  # Custom field to serialize 'target'
    timestamp = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S', read_only=True)  # Only read the timestamp

    class Meta:
        model = Notification
        fields =  ['id', 'recipient', 'actor', 'verb', 'target', 'is_read', 'timestamp']
    
     # Custom method to serialize the 'target' field (which is a GenericForeignKey)
    def get_target(self, obj):
        target_obj = obj.target

        if target_obj:
            return {
                'id': target_obj.id,
                'model': target_obj._meta.model_name,
                'data': str(target_obj) 
            }