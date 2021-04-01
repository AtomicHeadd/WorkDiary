# WorkDiary
作業時間を記録するPythonスクリプトです。  
現在は記録する機能しか実装されていません。  
A stopwatch that remembers time you spent on specific works.  
This script now only work in recording part(, doesn't work in statistics part).  

現在以下の問題が存在し、詳しくはコード内にコメントしています。  
いくつかの問題を修正しました。  
・~~日付の変化に未対応~~  
・~~正しい経過時間ではない(誤差<1分)~~  
・設定ファイルの文字をチェックしていない  
・~~ボタンの名前を日本語にすると読み込めずに立ち上がらない~~  
Some problems are left, which is written detailed in code.  
Fixed some known problems  
・~~Don't work over the days.~~  
・~~May contain extra time (under a minute).~~  
・Don't check string in setting file.  
・~~Non-English button name prevent execution.~~  
