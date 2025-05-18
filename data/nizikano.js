// 提取数据
const dialog = g_commu.logData.slice(1).map(item => item.chn_txt);

// 追加元素
if (g_commu.MyData[1]?.chn_txt) {
  dialog.push(g_commu.MyData[1].chn_txt);
}

// 保存文件
const blob = new Blob([dialog.join('\n')], { type: 'text/plain' });
const a = document.createElement('a');
a.href = URL.createObjectURL(blob);
a.download = 'dialogue.txt';
document.body.appendChild(a);
a.click();
document.body.removeChild(a);