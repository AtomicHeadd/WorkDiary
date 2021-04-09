# WorkDiary
作業時間を記録するPythonスクリプトです。  
現在は記録する機能しか実装されていません。  
A stopwatch that remembers time you spent on specific works.  
This script now only work in recording part(, doesn't work in statistics part).  

現在以下の問題が存在し、詳しくはコード内にコメントしています。  
・設定ファイルの文字をチェックしていない  
Some problems are left, which is written detailed in code.  
・Don't check string in setting file.  

今後実装したい機能
・統計画面
1. タスクごとの合計時間を一覧で表示する機能
2. タスクごとに日、月、年ごとの実行時間を表示する機能
・作業ボタンの増減機能
Fuctions planned to be implemented future develop.
・Statistics window
1. Show indivisual sum of time spent on the work.
2. Show indivisual sum of time based on daily, monthly and yealy.
・flexible button number

以下対応済みの問題
・日付の変化に未対応  
・正しい経過時間ではない(誤差<1分)  
・ボタンの名前を日本語にすると読み込めずに立ち上がらない  
