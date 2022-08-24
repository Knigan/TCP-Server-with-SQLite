import asyncio
import sqlite3
from sqlite3 import Error
        
def process(data):
    try:
        database = sqlite3.connect('Users.db')
        cursor = database.cursor()
        cursor.execute(data.decode())
        database.commit()
        rows = cursor.fetchall()
        result = '\n'
        for row in rows:
            result = result + str(row) + '\n'
        database.close()
        return result
        
    except Error:
        return "There was the error: " + str(Error)
    
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
        if result == '\n':
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


async def main(host, port):
    server = await asyncio.start_server(handle_connection, host, port)
    print(f"Start server...")
    async with server:
        await server.serve_forever()

HOST = "192.168.88.19"  # Symbolic name meaning all available interfaces
PORT = 5432  # Arbitrary non-privileged port

if __name__ == "__main__":
    asyncio.run(main(HOST, PORT))
