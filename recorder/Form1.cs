using Newtonsoft.Json;
using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Recorder
{
    public partial class RecorderForm : Form
    {
        HttpWebRequest hwr;
        public RecorderForm()
        {
            InitializeComponent();
        }

        private void HostSay_Click(object sender, EventArgs e)
        {
            Log.SelectionAlignment = HorizontalAlignment.Left;
            Log.AppendText(InputBox.Text);
            Log.AppendText("\n");
            InputBox.Clear();
            TulpaSay.Enabled = true;
            HostSay.Enabled = false;
        }

        private void TulpaSay_Click(object sender, EventArgs e)
        {
            Log.SelectionAlignment = HorizontalAlignment.Right;
            Log.AppendText(InputBox.Text);
            Log.AppendText("\n");
            InputBox.Clear();
            TulpaSay.Enabled = false;
            HostSay.Enabled = true;
        }

        private void SendReq(Object req)
        {
            this.hwr = (HttpWebRequest)WebRequest.Create("http://localhost:1224/");
            this.hwr.ContentType = "application/json; charset=UTF-8";
            this.hwr.Method = "POST";
            string req_str = JsonConvert.SerializeObject(req);
            byte[] bytes = Encoding.UTF8.GetBytes(req_str);
            this.hwr.ContentLength = bytes.Length;
            Stream writer = this.hwr.GetRequestStream();
            writer.Write(bytes, 0, bytes.Length);
            writer.Close();
            HttpWebResponse response = (HttpWebResponse)this.hwr.GetResponse();
            StreamReader reader = new StreamReader(response.GetResponseStream() ?? throw new InvalidOperationException(), Encoding.UTF8);
            string result = reader.ReadToEnd();
            response.Close();
            API_Response.AppendText(result);
            API_Response.AppendText("\n");
        }


        private void Send_Click(object sender, EventArgs e)
        {
            string[] Content = Log.Text.Split('\n');
            HostSay.Enabled = true;
            TulpaSay.Enabled = false;
            Log.Clear();
            Content = Content.Take(Content.Length - 1).ToArray();
            int max_size = Content.Length / 2;
            Content = Content.Take(max_size * 2).ToArray();
            string temp = "";
            ArrayList req_queue = new ArrayList(max_size);
            Sync_Request sync = new Sync_Request("");
            for(int i = 0; i < Content.Length; i++)
            {
                if (i % 2 == 0)
                {
                    temp = Content[i];
                }
                else
                {
                    Record_Request record = new Record_Request(temp, Content[i]);
                    req_queue.Add(record);
                }
            }
            API_Response.Clear();
            for(int i = 0; i < req_queue.Count; i++)
            {
                SendReq(req_queue[i]);
                SendReq(sync);
            }
        }
    }
    public class Record_Request
    {
        public string h;
        public string t;
        public Record_Request(string input_h, string input_t)
        {
            this.h = input_h;
            this.t = input_t;
        }
    }
    public class Sync_Request
    {
        public string sync;

        public Sync_Request(string input_sync)
        {
            this.sync = input_sync;
        }
    }

}
