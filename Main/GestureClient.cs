using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace TuioDemo
{
    public interface GestureListener
    {
        /**
         * <summary>
         * This callback method is invoked by the TuioClient when a new TuioObject is added to the session.</summary>
         *
         * <param name="tobj">the TuioObject reference associated to the addTuioObject event</param>
         */
        // void OnConnected();

        void OnGestureUpdate(string gesture);
    }
    class GestureClient
    {
        int byteCT;
        public NetworkStream stream;
        byte[] sendData;
        public TcpClient client;
        private Thread thread;
        private bool connected;
        private GestureListener listener = null;
        public void setListener(GestureListener listener)
        {
            this.listener = listener;
        }
        private void listen()
        {
            while (connected)
            {
                try
                {

                    byte[] receiveBuffer = new byte[1024];
                    int bytesReceived = stream.Read(receiveBuffer, 0, 1024);
                    string data = Encoding.UTF8.GetString(receiveBuffer, 0, bytesReceived);
                    Console.WriteLine(data);
                    listener.OnGestureUpdate(data);
                }
                catch (System.Exception e)
                {
                    Console.WriteLine("error {0}", e);
                }
            }
        }
        public bool isConnected() { return connected; }
        public void connect(int portNumber)
        {
            if (listener == null)
                throw new Exception("are you trolling where is ur listener m8");
            try
            {
                client = new TcpClient("localhost", portNumber);
                stream = client.GetStream();
                Console.WriteLine("connection made ! with " + "localhost");
                connected = true;
                thread = new Thread(new ThreadStart(listen));
                thread.Start();
            }
            catch (Exception e)
            {
                Console.WriteLine("failed to connect to port " + portNumber);
                Console.WriteLine(e.Message);
            }
        }

        /*public bool connectToSocket(string host, int portNumber)
        {
            try
            {
                client = new TcpClient(host, portNumber);
                stream = client.GetStream();
                Console.WriteLine("connection made ! with " + host);
                return true;
            }
            catch (System.Net.Sockets.SocketException e)
            {
                Console.WriteLine("Connection Failed: " + e.Message);
                return false;
            }
        }*/

        public string recieveMessage()
        {
            try
            {

                byte[] receiveBuffer = new byte[1024];
                int bytesReceived = stream.Read(receiveBuffer, 0, 1024);
                Console.WriteLine(bytesReceived);
                string data = Encoding.UTF8.GetString(receiveBuffer, 0, bytesReceived);
                Console.WriteLine(data);
                return data;
            }
            catch (System.Exception e)
            {

            }

            return null;
        }
    }
}