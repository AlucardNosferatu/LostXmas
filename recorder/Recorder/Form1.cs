using Newtonsoft.Json;
using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Recorder
{
    public partial class RecorderForm : Form
    {
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
            for(int i = 0; i < Content.Length; i++)
            {
                if (i % 2 == 0)
                {
                    temp = Content[i];
                }
                else
                {
                    API_Request req = new API_Request(temp, Content[i]);
                    req_queue.Add(req);
                }
            }
            API_Response.Clear();
            for(int i = 0; i < req_queue.Count; i++)
            {
                API_Response.AppendText(JsonConvert.SerializeObject(req_queue[i]));
                API_Response.AppendText("\n");
            }
        }
    }
    public class API_Request
    {
        public string h;
        public string t;
        public API_Request(string input_h, string input_t)
        {
            this.h = input_h;
            this.t = input_t;
        }
    }
}
