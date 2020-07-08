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
            this.HostSay = new System.Windows.Forms.Button();
            this.TulpaSay = new System.Windows.Forms.Button();
            this.Send = new System.Windows.Forms.Button();
            this.flowLayoutPanel2 = new System.Windows.Forms.FlowLayoutPanel();
            this.KeyLabel = new System.Windows.Forms.Label();
            this.InputKey = new System.Windows.Forms.TextBox();
            this.ValLabel = new System.Windows.Forms.Label();
            this.InputVal = new System.Windows.Forms.TextBox();
            this.Append = new System.Windows.Forms.Button();
            this.Submit = new System.Windows.Forms.Button();
            this.JsonTree = new System.Windows.Forms.TreeView();
            this.flowLayoutPanel1.SuspendLayout();
            this.flowLayoutPanel2.SuspendLayout();
            this.SuspendLayout();
            // 
            // Log
            // 
            this.Log.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.Log.Location = new System.Drawing.Point(16, 15);
            this.Log.Margin = new System.Windows.Forms.Padding(4);
            this.Log.Name = "Log";
            this.Log.Size = new System.Drawing.Size(502, 351);
            this.Log.TabIndex = 0;
            this.Log.Text = "";
            // 
            // InputBox
            // 
            this.InputBox.Location = new System.Drawing.Point(16, 374);
            this.InputBox.Margin = new System.Windows.Forms.Padding(4);
            this.InputBox.Name = "InputBox";
            this.InputBox.Size = new System.Drawing.Size(776, 25);
            this.InputBox.TabIndex = 1;
            // 
            // API_Response
            // 
            this.API_Response.Location = new System.Drawing.Point(169, 407);
            this.API_Response.Margin = new System.Windows.Forms.Padding(4);
            this.API_Response.Name = "API_Response";
            this.API_Response.Size = new System.Drawing.Size(501, 186);
            this.API_Response.TabIndex = 4;
            this.API_Response.Text = "";
            // 
            // flowLayoutPanel1
            // 
            this.flowLayoutPanel1.AutoSize = true;
            this.flowLayoutPanel1.Controls.Add(this.HostSay);
            this.flowLayoutPanel1.Controls.Add(this.TulpaSay);
            this.flowLayoutPanel1.Controls.Add(this.Send);
            this.flowLayoutPanel1.FlowDirection = System.Windows.Forms.FlowDirection.TopDown;
            this.flowLayoutPanel1.Location = new System.Drawing.Point(13, 407);
            this.flowLayoutPanel1.Margin = new System.Windows.Forms.Padding(4);
            this.flowLayoutPanel1.Name = "flowLayoutPanel1";
            this.flowLayoutPanel1.Padding = new System.Windows.Forms.Padding(7);
            this.flowLayoutPanel1.Size = new System.Drawing.Size(148, 186);
            this.flowLayoutPanel1.TabIndex = 6;
            // 
            // HostSay
            // 
            this.HostSay.AutoSize = true;
            this.HostSay.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.HostSay.Font = new System.Drawing.Font("宋体", 22.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.HostSay.Location = new System.Drawing.Point(11, 11);
            this.HostSay.Margin = new System.Windows.Forms.Padding(4);
            this.HostSay.Name = "HostSay";
            this.HostSay.Size = new System.Drawing.Size(103, 48);
            this.HostSay.TabIndex = 2;
            this.HostSay.Text = "Host";
            this.HostSay.UseVisualStyleBackColor = true;
            this.HostSay.Click += new System.EventHandler(this.HostSay_Click);
            // 
            // TulpaSay
            // 
            this.TulpaSay.AutoSize = true;
            this.TulpaSay.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.TulpaSay.Enabled = false;
            this.TulpaSay.Font = new System.Drawing.Font("宋体", 22.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.TulpaSay.Location = new System.Drawing.Point(11, 67);
            this.TulpaSay.Margin = new System.Windows.Forms.Padding(4);
            this.TulpaSay.Name = "TulpaSay";
            this.TulpaSay.Size = new System.Drawing.Size(122, 48);
            this.TulpaSay.TabIndex = 3;
            this.TulpaSay.Text = "Tulpa";
            this.TulpaSay.UseVisualStyleBackColor = true;
            this.TulpaSay.Click += new System.EventHandler(this.TulpaSay_Click);
            // 
            // Send
            // 
            this.Send.AutoSize = true;
            this.Send.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.Send.Font = new System.Drawing.Font("宋体", 22.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Send.Location = new System.Drawing.Point(11, 123);
            this.Send.Margin = new System.Windows.Forms.Padding(4);
            this.Send.Name = "Send";
            this.Send.Size = new System.Drawing.Size(103, 48);
            this.Send.TabIndex = 5;
            this.Send.Text = "Send";
            this.Send.UseVisualStyleBackColor = true;
            this.Send.Click += new System.EventHandler(this.Send_Click);
            // 
            // flowLayoutPanel2
            // 
            this.flowLayoutPanel2.AutoSize = true;
            this.flowLayoutPanel2.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.flowLayoutPanel2.Controls.Add(this.KeyLabel);
            this.flowLayoutPanel2.Controls.Add(this.InputKey);
            this.flowLayoutPanel2.Controls.Add(this.ValLabel);
            this.flowLayoutPanel2.Controls.Add(this.InputVal);
            this.flowLayoutPanel2.Controls.Add(this.Append);
            this.flowLayoutPanel2.Controls.Add(this.Submit);
            this.flowLayoutPanel2.FlowDirection = System.Windows.Forms.FlowDirection.TopDown;
            this.flowLayoutPanel2.Location = new System.Drawing.Point(678, 409);
            this.flowLayoutPanel2.Margin = new System.Windows.Forms.Padding(4);
            this.flowLayoutPanel2.Name = "flowLayoutPanel2";
            this.flowLayoutPanel2.Size = new System.Drawing.Size(114, 184);
            this.flowLayoutPanel2.TabIndex = 7;
            // 
            // KeyLabel
            // 
            this.KeyLabel.AutoSize = true;
            this.KeyLabel.Location = new System.Drawing.Point(3, 0);
            this.KeyLabel.Name = "KeyLabel";
            this.KeyLabel.Size = new System.Drawing.Size(31, 15);
            this.KeyLabel.TabIndex = 8;
            this.KeyLabel.Text = "Key";
            // 
            // InputKey
            // 
            this.InputKey.Location = new System.Drawing.Point(3, 18);
            this.InputKey.Name = "InputKey";
            this.InputKey.Size = new System.Drawing.Size(107, 25);
            this.InputKey.TabIndex = 7;
            // 
            // ValLabel
            // 
            this.ValLabel.AutoSize = true;
            this.ValLabel.Location = new System.Drawing.Point(3, 46);
            this.ValLabel.Name = "ValLabel";
            this.ValLabel.Size = new System.Drawing.Size(31, 15);
            this.ValLabel.TabIndex = 9;
            this.ValLabel.Text = "Val";
            // 
            // InputVal
            // 
            this.InputVal.Location = new System.Drawing.Point(3, 64);
            this.InputVal.Name = "InputVal";
            this.InputVal.Size = new System.Drawing.Size(107, 25);
            this.InputVal.TabIndex = 10;
            // 
            // Append
            // 
            this.Append.AutoSize = true;
            this.Append.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.Append.Font = new System.Drawing.Font("宋体", 16.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Append.Location = new System.Drawing.Point(4, 96);
            this.Append.Margin = new System.Windows.Forms.Padding(4);
            this.Append.Name = "Append";
            this.Append.Size = new System.Drawing.Size(106, 38);
            this.Append.TabIndex = 5;
            this.Append.Text = "Append";
            this.Append.UseVisualStyleBackColor = true;
            this.Append.Click += new System.EventHandler(this.Append_Click);
            // 
            // Submit
            // 
            this.Submit.AutoSize = true;
            this.Submit.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.Submit.Font = new System.Drawing.Font("宋体", 16.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Submit.Location = new System.Drawing.Point(4, 142);
            this.Submit.Margin = new System.Windows.Forms.Padding(4);
            this.Submit.Name = "Submit";
            this.Submit.Size = new System.Drawing.Size(106, 38);
            this.Submit.TabIndex = 6;
            this.Submit.Text = "Submit";
            this.Submit.UseVisualStyleBackColor = true;
            this.Submit.Click += new System.EventHandler(this.Submit_Click);
            // 
            // JsonTree
            // 
            this.JsonTree.Location = new System.Drawing.Point(526, 15);
            this.JsonTree.Name = "JsonTree";
            this.JsonTree.Size = new System.Drawing.Size(266, 351);
            this.JsonTree.TabIndex = 8;
            // 
            // RecorderForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.ClientSize = new System.Drawing.Size(809, 606);
            this.Controls.Add(this.API_Response);
            this.Controls.Add(this.JsonTree);
            this.Controls.Add(this.flowLayoutPanel2);
            this.Controls.Add(this.flowLayoutPanel1);
            this.Controls.Add(this.InputBox);
            this.Controls.Add(this.Log);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Margin = new System.Windows.Forms.Padding(4);
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "RecorderForm";
            this.Text = "Recorder";
            this.flowLayoutPanel1.ResumeLayout(false);
            this.flowLayoutPanel1.PerformLayout();
            this.flowLayoutPanel2.ResumeLayout(false);
            this.flowLayoutPanel2.PerformLayout();
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
        private System.Windows.Forms.FlowLayoutPanel flowLayoutPanel2;
        private System.Windows.Forms.Button Append;
        private System.Windows.Forms.Button Submit;
        private System.Windows.Forms.TextBox InputKey;
        private System.Windows.Forms.Label KeyLabel;
        private System.Windows.Forms.Label ValLabel;
        private System.Windows.Forms.TextBox InputVal;
        private System.Windows.Forms.TreeView JsonTree;
    }
}

