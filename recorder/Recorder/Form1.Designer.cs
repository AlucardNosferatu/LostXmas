namespace Recorder
{
    partial class RecorderForm
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(RecorderForm));
            this.Log = new System.Windows.Forms.RichTextBox();
            this.InputBox = new System.Windows.Forms.TextBox();
            this.API_Response = new System.Windows.Forms.RichTextBox();
            this.flowLayoutPanel1 = new System.Windows.Forms.FlowLayoutPanel();
            this.TulpaSay = new System.Windows.Forms.Button();
            this.Send = new System.Windows.Forms.Button();
            this.HostSay = new System.Windows.Forms.Button();
            this.flowLayoutPanel1.SuspendLayout();
            this.SuspendLayout();
            // 
            // Log
            // 
            this.Log.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.Log.Location = new System.Drawing.Point(12, 12);
            this.Log.Name = "Log";
            this.Log.Size = new System.Drawing.Size(583, 277);
            this.Log.TabIndex = 0;
            this.Log.Text = "";
            // 
            // InputBox
            // 
            this.InputBox.Location = new System.Drawing.Point(12, 295);
            this.InputBox.Name = "InputBox";
            this.InputBox.Size = new System.Drawing.Size(583, 21);
            this.InputBox.TabIndex = 1;
            // 
            // API_Response
            // 
            this.API_Response.Location = new System.Drawing.Point(139, 322);
            this.API_Response.Name = "API_Response";
            this.API_Response.Size = new System.Drawing.Size(456, 153);
            this.API_Response.TabIndex = 4;
            this.API_Response.Text = "";
            // 
            // flowLayoutPanel1
            // 
            this.flowLayoutPanel1.AutoSize = true;
            this.flowLayoutPanel1.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.flowLayoutPanel1.Controls.Add(this.HostSay);
            this.flowLayoutPanel1.Controls.Add(this.TulpaSay);
            this.flowLayoutPanel1.Controls.Add(this.Send);
            this.flowLayoutPanel1.FlowDirection = System.Windows.Forms.FlowDirection.TopDown;
            this.flowLayoutPanel1.Location = new System.Drawing.Point(12, 322);
            this.flowLayoutPanel1.Name = "flowLayoutPanel1";
            this.flowLayoutPanel1.Size = new System.Drawing.Size(121, 153);
            this.flowLayoutPanel1.TabIndex = 6;
            // 
            // TulpaSay
            // 
            this.TulpaSay.AutoSize = true;
            this.TulpaSay.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.TulpaSay.Enabled = false;
            this.TulpaSay.Font = new System.Drawing.Font("宋体", 26.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.TulpaSay.Location = new System.Drawing.Point(3, 54);
            this.TulpaSay.Name = "TulpaSay";
            this.TulpaSay.Size = new System.Drawing.Size(115, 45);
            this.TulpaSay.TabIndex = 3;
            this.TulpaSay.Text = "Tulpa";
            this.TulpaSay.UseVisualStyleBackColor = true;
            this.TulpaSay.Click += new System.EventHandler(this.TulpaSay_Click);
            // 
            // Send
            // 
            this.Send.AutoSize = true;
            this.Send.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.Send.Font = new System.Drawing.Font("宋体", 26.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Send.Location = new System.Drawing.Point(3, 105);
            this.Send.Name = "Send";
            this.Send.Size = new System.Drawing.Size(97, 45);
            this.Send.TabIndex = 5;
            this.Send.Text = "Send";
            this.Send.UseVisualStyleBackColor = true;
            this.Send.Click += new System.EventHandler(this.Send_Click);
            // 
            // HostSay
            // 
            this.HostSay.AutoSize = true;
            this.HostSay.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.HostSay.Font = new System.Drawing.Font("宋体", 26.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.HostSay.Location = new System.Drawing.Point(3, 3);
            this.HostSay.Name = "HostSay";
            this.HostSay.Size = new System.Drawing.Size(97, 45);
            this.HostSay.TabIndex = 2;
            this.HostSay.Text = "Host";
            this.HostSay.UseVisualStyleBackColor = true;
            this.HostSay.Click += new System.EventHandler(this.HostSay_Click);
            // 
            // RecorderForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(607, 485);
            this.Controls.Add(this.flowLayoutPanel1);
            this.Controls.Add(this.API_Response);
            this.Controls.Add(this.InputBox);
            this.Controls.Add(this.Log);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "RecorderForm";
            this.Text = "Recorder";
            this.flowLayoutPanel1.ResumeLayout(false);
            this.flowLayoutPanel1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.RichTextBox Log;
        private System.Windows.Forms.TextBox InputBox;
        private System.Windows.Forms.RichTextBox API_Response;
        private System.Windows.Forms.FlowLayoutPanel flowLayoutPanel1;
        private System.Windows.Forms.Button HostSay;
        private System.Windows.Forms.Button Send;
        private System.Windows.Forms.Button TulpaSay;
    }
}

