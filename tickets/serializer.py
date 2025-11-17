from rest_framework import serializers
from .models import Ticket, TicketEvent

class TicketEventSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TicketEvent
        fields = ["id", "event_type", "author_name", "message", "from_status", "to_status", "created_at"]
        read_only_fields = ["id", "event_type", "author_name", "from_status", "to_status", "created_at"]

    def get_author_name(self, obj):
        return getattr(obj.author, "username", None)

class TicketSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    events = TicketEventSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id", "title", "description", "order_reference",
            "status", "priority", "created_by", "assigned_to",
            "created_at", "updated_at", "events"
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at", "events"]

class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["title", "description", "priority", "assigned_to"]