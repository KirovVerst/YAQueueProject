using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MailClient
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private async void button1_Click(object sender, EventArgs e)
        {
            HttpClient client = new HttpClient();
            string baseUrl = "kirov.verst.service@gmail.com";
            string email_from, subject, text;
            email_from = emailForm.Text;
            subject = "Отзыв";
            text = TextMessageForm.Text;

            var values = new Dictionary<string, string>
                {
                   { "email_from", email_from },
                   { "email_to", "kirov.verst.service@gmail.com" },
                   { "subject", "Отзыв" },
                   { "text", text }
                };

            var content = new FormUrlEncodedContent(values);

            var response = await client.PostAsync("http://207.154.238.238:80/api/api/mailgun/email/", content);

            var responseString = await response.Content.ReadAsStringAsync();
        }

        private void richTextBox1_TextChanged(object sender, EventArgs e)
        {


        }
    }
}
