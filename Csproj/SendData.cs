using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.IO;

namespace MyGameMod
{
    class SendData
    {
        static bool ServerRunning = false;
        private static TcpListener server;

        public static void Python(string[] args)
        {
            GameMod.logger.LogInfo("starting server");
            if (ServerRunning == false)
            {
                ServerRunning = true;
                // Start the server thread
                GameMod.logger.LogInfo("created thread");
                Thread serverThread = new Thread(() =>
                {
                    try
                    {
                        // Initialize and start the server on the separate thread
                        IPAddress ipAddress = IPAddress.Parse("127.0.0.1"); // Replace with your desired IP
                        server = new TcpListener(ipAddress, 8008);
                        server.Start();
                        Console.WriteLine($"Server started on {ipAddress}:8008");

                        while (ServerRunning == true)
                        {
                            if (!server.Pending())
                            {
                                Thread.Sleep(100); // No pending connections, sleep for a short duration
                                continue;
                            }

                            GameMod.logger.LogInfo("Waiting for client connection...");
                            TcpClient client = null;
                            NetworkStream stream = null;

                            // Attempt to connect to the client
                            while (client == null)
                            {
                                try
                                {
                                    client = server.AcceptTcpClient();
                                    stream = client.GetStream();
                                    GameMod.logger.LogInfo("Client connected!");
                                }
                                catch (Exception ex)
                                {
                                    GameMod.logger.LogError($"Error accepting client: {ex.Message}");
                                    Thread.Sleep(1000); // Retry after 1 second
                                }
                            }

                            // Handle client connection
                            while (ServerRunning && client.Connected)
                            {
                                try
                                {
                                    if (!string.IsNullOrEmpty(GameMod.PythonData) && GameMod.PythonData != "[]" && !string.IsNullOrWhiteSpace(GameMod.PythonData))
                                    {
                                        GameMod.logger.LogInfo($"PythonData: {GameMod.PythonData}");
                                        byte[] data = Encoding.UTF8.GetBytes(GameMod.PythonData);
                                        stream.Write(data, 0, data.Length);
                                        GameMod.logger.LogInfo("Data sent.");
                                        GameMod.PythonData = string.Empty; // Clear the PythonData string
                                    }
                                    else
                                    {
                                    }
                                }
                                catch (Exception ex)
                                {
                                    GameMod.logger.LogError($"Error writing to stream: {ex.Message}");
                                    client.Close(); // Close client connection on error
                                    break; // Exit the inner loop to reattempt connection
                                }
                            }

                            client.Close(); // Close client connection when done
                            GameMod.logger.LogInfo("Client connection closed.");
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"Error starting server: {ex.Message}");
                        ServerRunning = false;
                    }
                });

                serverThread.Start();
            }
        }
    }
}





