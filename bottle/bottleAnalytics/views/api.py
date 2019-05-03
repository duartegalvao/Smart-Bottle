import traceback
from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bottleAnalytics.models import BottleReading


@api_view(['POST'])
def bottle_update(request):
    """Receive data from the bottle"""
    try:
        data = request.data['data']

        n_errors = 0
        for data_point in data:
            try:
                bottle_reading = BottleReading()
                bottle_reading.temp = data_point['temp']
                bottle_reading.weight = data_point['weight']
                bottle_reading.time = datetime.fromtimestamp(data_point['time'])
                bottle_reading.save()
            except KeyError or TypeError:
                #  Ignore errors inside batch, accepting all successful
                # data points and registering
                n_errors += 1

        return Response({
                            "status": "updated",
                            "n_errors": n_errors,
                        }, status=status.HTTP_200_OK)

    except KeyError:
        return Response({
            "status": "keyError",
        }, status=status.HTTP_400_BAD_REQUEST)
    except TypeError:
        print(traceback.format_exc())
        return Response({
            "status": "typeError",
        }, status=status.HTTP_400_BAD_REQUEST)

# TEST bottleUpdate
# curl --data "temp=10&weight=11" localhost:8000/api/bottleUpdate
