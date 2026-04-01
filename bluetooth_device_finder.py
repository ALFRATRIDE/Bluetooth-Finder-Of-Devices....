def bluetooth_finder(print_chars: bool | None = None):
    """
    Finds bluetooth devices ? I think ? idrk tbh. . .
    \n
    IT BURNS (<-- Original Name of this Project)
    """
    try:
        import bleak, asyncio
        import colorama
    except (ImportError, Exception) as err:
        print(f"ImportError: {err}")

    DEVICE_TYPE = {
        0: "Unknown",
        64: "Phone",
        128: "Computer",
        192: "Watch",
        193: "Sports Watch",
        256: "Clock",
        320: "Display",
        384: "Remote Control",
        448: "Glasses",
        512: "Tag",
        576: "Keyring",
        640: "Media Player",
        704: "Barcode Scanner",
        768: "Thermometer",
        832: "Heart Rate Sensor",
        896: "Blood Pressure",
        960: "HID Generic",
        961: "Keyboard",
        962: "Mouse",
        963: "Joystick",
        964: "Gamepad",
        1152: "Glucose Meter",
        1216: "Running/Walking Sensor",
        1280: "Cycling",
        1344: "Control Device",
        1408: "Network Device",
        1472: "Sensor",
        1536: "Light Fixture",
        1600: "Fan",
        1664: "HVAC",
        1728: "Air Conditioning",
        1792: "Humidifier",
        1856: "Heating",
        3136: "Pulse Oximeter",
        3200: "Weight Scale",
        3264: "Personal Mobility Device",
        5184: "Insulin Pump",
    }

    async def get_type(client: bleak.BleakClient):
        try:
            data = await client.read_gatt_char("2a01")
            code = int.from_bytes(data, "little")
            return DEVICE_TYPE.get(code, f"Unknown (code: {code})")
        except Exception:
            print(colorama.Fore.RED + "Could not read. . ?")


    async def try_read(client: bleak.BleakClient, *uuids):
        for uuid in uuids:
            try:
                data = await client.read_gatt_char(uuid)
                return data
            except Exception:
                continue
        return None

    async def inspect(device):
        print("#" * 3, "Inspecting. . .")
        try:
            async with bleak.BleakClient(device, timeout=10.0) as client:
                device_type = await get_type(client)
                print(colorama.Fore.MAGENTA + f"Device Type: {device_type}")
                
                for service in client.services:
                    print(f"\nService: {service.uuid}")

                    readable = [c.uuid for c in service.characteristics if "read" in c.properties]
                    
                    if print_chars or print_chars is None:
                        for character in service.characteristics:
                            print(colorama.Fore.YELLOW + f"Char: {character.uuid} | {character.properties}")
                    else:
                        print(colorama.Fore.YELLOW + f"you don't like Chars ???")

                    name = await try_read(client, *readable)
                    if name:
                        try:
                            print(colorama.Fore.MAGENTA + f"\nData: {name.decode(errors = 'ignore')}")
                        except:
                            print(f"Raw bytes: {name}")
        except TimeoutError:
            print(colorama.Fore.RED + "connection time out")
        except Exception as exc:
            print(colorama.Fore.RED + f"exception: {exc}")

    async def scan():
        print(colorama.Fore.WHITE + "Scanning. . .")
        devices = await bleak.BleakScanner.discover(timeout=5.0)

        for device in devices:
            print(colorama.Fore.CYAN + f"Name: {device.name}")
            print(colorama.Fore.GREEN + f"Address: {device.address}")
            await inspect(device)
            print(colorama.Fore.WHITE + "-" * 50)

        return device.name, device.address
            
    asyncio.run(scan())
    return "Nothing :3c"

if __name__ == '__main__':
    bluetooth_finder()
    #bluetooth_finder(True)
    #bluetooth_finder(False)

# this GENUINELY was so annoying to make ;-;