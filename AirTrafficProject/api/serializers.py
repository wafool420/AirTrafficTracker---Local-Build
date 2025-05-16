from rest_framework import serializers 
from AirTrafficApp.models import Items

class ItemSerializer(serializers.ModelSerializer):
    timeliness = serializers.CharField()
    bird_strike = serializers.CharField()
    runway_incursion = serializers.CharField()

    class Meta:
        model = Items
        fields = [
            'date_of_operation', 'call_sign', 'aircraft_type', 'detail',
            'origin', 'destination', 'route_of_flight', 'actual_time',
            'timeliness', 'type_of_flight', 'genav_detail', 'bird_strike',
            'runway_incursion', 'movement', 'user'
        ]

    def validate(self, data):
        flight_type = data.get("type_of_flight")
        actual_time = data.get("actual_time")
        timeliness = data.get("timeliness")
        bird_strike = data.get("bird_strike")
        runway_incursion = data.get("runway_incursion")
        movement = data.get("movement")
        
        # Ensure that the values are properly prefixed
        if flight_type:
            # Validate Timeliness
            valid_timeliness = [
                f"{flight_type} Delayed",
                f"{flight_type} On Time",
                f"{flight_type} N/A"
            ]
            if timeliness not in valid_timeliness:
                raise serializers.ValidationError({
                    "timeliness": f"{timeliness} is not a valid choice for {flight_type}."
                })

            # Validate Bird Strike
            if bird_strike.lower() not in ["yes", "no"]:
                raise serializers.ValidationError({
                    "bird_strike": "Bird Strike must be either 'yes' or 'no'."
                })
            else:
                data["bird_strike"] = f"{flight_type} {movement} {bird_strike}"

            if runway_incursion.lower() not in ["yes", "no"]:
                raise serializers.ValidationError({
                    "runway_incursion": "Runway Incursion must be either 'yes' or 'no'."
                })
            else:
                data["runway_incursion"] = f"{flight_type} {movement} {runway_incursion}"

            if actual_time:
                data["actual_time"] = f"{flight_type} {actual_time}"

            if flight_type != "GenAv":
                data["genav_detail"] = "N/A"

        return data
