-- VCの入退室ログ
DROP TABLE vc_access_records;
CREATE TABLE vc_access_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- サロゲートキー
    member_id TEXT,                         -- Discord Member ID
    member_name TEXT,                       -- Discord Member Name
    member_discriminator TEXT,              -- Discord Member Discriminator #0000 みたいなやつ
    in_datetime TEXT,                       -- 入室日時
    out_datetime TEXT,                      -- 退室日時
    stay_second INT                         -- 滞在時間
);
