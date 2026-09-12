# 第一原理：公開案例

下列公開事件用來說明查核方法。建議檢查是依來源整理的工程啟示；社群版未包含
私人專案事件或實驗結果。

## Knight Capital：部署不完整

SEC（美國證券交易委員會）發現新程式部署到八台伺服器中的七台，另一台仍保留
可被呼叫的 Power Peg 程式。重新使用的旗標啟動舊程式；處理期間移除其他
伺服器的新程式，使事故擴大。依賴部署假設前，逐一確認目標版本及重用旗標的行為。

來源：[SEC Release 34-70694，第 13–17 段](https://www.sec.gov/Archives/edgar/data/1569391/000119312513401173/d613486dex101.htm)。

## Mars Climate Orbiter：介面單位

NASA/JPL 的初步調查指出，以英制單位提供的資料傳入預期公制單位的導航系統。
檢查資料產生端的實際單位是否符合接收端契約，包含跨團隊的整合檢查。

來源：[NASA/JPL，1999 年 9 月 30 日](https://www.jpl.nasa.gov/news/mars-climate-orbiter-team-finds-likely-cause-of-loss/)。

## Heartbleed：未檢查輸入長度

OpenSSL 公告說明，TLS heartbeat（連線心跳訊息）的處理缺少邊界檢查，可能
洩漏行程記憶體。將不可信輸入提供的長度與實際緩衝區大小比較；函式庫的聲譽
不能證明該路徑已受到測試涵蓋。

來源：[OpenSSL 安全公告，2014 年 4 月 7 日](https://openssl-library.org/news/secadv/20140407.txt)。
