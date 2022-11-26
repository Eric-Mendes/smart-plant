from .extract_thingsboard import DriversThingsBoard
import json

def test_extractor_thingsboard()-> None:
    """teste de extração de arquivos no formato xlsx"""
    extractor_things_board = DriversThingsBoard


    token = extractor_things_board.getToken("mc855.projeto.5@gmail.com", "vaX7Og1ehO74bFB")

    devices_ids = extractor_things_board.getDevices(token)

    unity_table = {
        "temperature": "celcius - checar",
        "humidity": "g/m³ - checar",
        "distance": "m - checar"
    }

    data = []

    for device_id in devices_ids:
        result = extractor_things_board.getTelemetry(device_id, token)
        for key in result.keys():
                data.append({
                    "sensor_id": device_id,
                    "type": key,
                    "value": result[key][0]["value"],
                    "unity": unity_table[key],
                    "located_at": None,
                    "inserted_at": result[key][0]["ts"],
                    "updated_at": result[key][0]["ts"]
                })

    print(json.dumps(data))

