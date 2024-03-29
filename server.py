import asyncio
import sqlite3
from sqlite3 import Error
        
def process(data):
    try:
        database = sqlite3.connect('MessengerDB.db')
        cursor = database.cursor()
        cursor.execute(data.decode())
        database.commit()
        rows = cursor.fetchall()
        result = ""
        for row in rows:
            result = result + str(row) + "[?~?]"
        database.close()
        return result
        
    except Error:
        return str(Error)
    
async def handle_connection(reader, writer):
    addr = writer.get_extra_info("peername")
    print("Connected by", addr)
    while True:
        # Receive
        try:
            data = await reader.read(1024)  # New
        except ConnectionError:
            print(f"Client suddenly closed while receiving from {addr}")
            break
        print(f"Received {data} from: {addr}")
        if not data:
            break
        # Process
        result = str(process(data))
        if result == "":
            data = "The request was completed successfully".encode()
        else:
            data = result.encode()
        # Send
        print(f"Send: {data} to: {addr}")
        try:
            writer.write(data)  # New
            await writer.drain()
        except ConnectionError:
            print(f"Client suddenly closed, cannot send")
            break
    writer.close()
    print("Disconnected by", addr)
    print('\n')


async def main(host, port):
    server = await asyncio.start_server(handle_connection, host, port)
    print(f"Start server...")
    async with server:
        await server.serve_forever()

HOST = "192.168.88.254"  # Symbolic name meaning all available interfaces
PORT = 31416  # Arbitrary non-privileged port

if __name__ == "__main__":
    asyncio.run(main(HOST, PORT))
