/**
 * 今回テーブルは二つ用意
 * "AddressTable"と"idTable"
 * "AddressTable"は今回のDBの本体で電話帳の役割
 * "idTable"は新規登録のためのID管理用DB
 * "idTable"の中にはデータを削除したIDと現在使用しているIDのなかで一番大きいIDの次のIDを登録
 */
'use strict';

// MySQLに接続
var mysql = require('mysql');

/** DB接続用関数（MySQL情報）*/ 
function Connect(connecteInfo) {
  // MySQLに接続
  var connection = mysql.createConnection(connecteInfo);
  connection.connect(function (err) {
    if(err){
      console.log(err.stack);
      return;
    }
    console.log('success');
  });
  return connection;
}

/** データ引き出し用関数（条件の値（json形式），MySQL情報）※検索する条件はどれでも可能*/
function PullData(value, connecteInfo){
  // MySQLに接続
  var connection = Connect(connecteInfo);
  var resultList = [];
  // MySQLコマンドの作成
  var Query = 'SELECT * FROM AddressTable where ';
  var keys = Object.keys(value);
  for(const index in keys){
    if(index > 0){
      Query += ' and';
    }
    Query += (' ' + keys[index] + '=?');
  }
  // データの引き出し
  connection.query(Query, Object.values(value),function (error, results, fields) { 
    var len = results.length;
    // データが空か判定
    if(len > 0){
      for(var i = 0; i < len; i++){
        // json形式でデータを格納
        resultList[i] = {
          name:results[i].name,
          mail:results[i].mail,
          color:results[i].color,
          flag:results[i].flag
        };
      }        
    }
    // この関数は非同期であるためここからのみデータの出力が可能
    console.log('PullData');
    console.log(resultList);
  });
  // MySQLとの接続を切断
  connection.end();
}

/** データ登録用関数（登録データ（json形式），MySQL情報）※メールアドレスが一致するものは通知する仕様 */
function Registration(value, connecteInfo){
  // MySQLに接続
  var connection = Connect(connecteInfo);
  // MySQLコマンドの作成
  var selectQuery = 'SELECT * FROM AddressTable where mail=?';
  // メールアドレスが一致するものがあるか確認
  connection.query(selectQuery, value.mail,function (error, results, fields) {
    console.log('PullData of Registration'); 
    console.log(results);
    var len = results.length;
    // 一致するものがない場合新規登録処理
    if(len == 0){
      // MySQLに接続
      var co = Connect(connecteInfo);
      var idQuery = 'SELECT * FROM idTable WHERE id=(SELECT MIN(id) FROM idTable)';
      // データを新規登録
      co.query(idQuery, function (error, res, fields) { 
        // IDを付与
        value.id = res[0].id;
        console.log(value);

        // MySQLに接続
        var conn = Connect(connecteInfo);
        // MySQLコマンドの作成
        var insertQuery = 'INSERT INTO AddressTable set ?';
        // データを新規登録
        conn.query(insertQuery, value,function (error, r, fields) { 
          console.log('Insert：' + r);
        });
        // MySQLとの接続を切断
        conn.end();

        // MySQLに接続
        var idConnect = Connect(connecteInfo);
        if(res[0].name == 'next'){
          // MySQLコマンドの作成
          var Query = "UPDATE idTable SET id=? where name=?";
          var nextID = value.id + 1;
          console.log(nextID);
          // IDデータを更新
          idConnect.query(Query, [nextID, res[0].name],function (error, r, fields) { 
            console.log('UpdateIdTable：' + r);
          });         
        }

        else{
          // MySQLコマンドの作成
          var Query = "DELETE FROM idTable where id=?";
          // IDデータを削除
          idConnect.query(Query, [value.id],function (error, r, fields) { 
            console.log('DeleteIdTable：' + r);
          });             
        }
        // MySQLとの接続を切断
        idConnect.end();       
      });
      // MySQLとの接続を切断
      co.end();
    }
    // 一致するものがある場合通知
    else{
      console.log(results[0].id + 'に登録済みのメールアドレスです．');
    }
  });
  connection.end();
}

/** データ更新用関数（更新データ（json形式），MySQL情報）※更新データにはID情報が必須 */
function UpdateMail(value, connecteInfo) {
  // MySQLに接続
  var connection = Connect(connecteInfo);
  // MySQLコマンドの作成
  var Query = 'UPDATE AddressTable SET ? where id=?';
  // データを更新
  connection.query(Query, [value, value.id],function (error, res, fields) { 
    console.log('UpdateMail：' + res);
  });
  connection.end();
}

/** データ削除用関数（削除対象ID（配列），MySQL情報）※ID情報で対象を指定，複数指定可能　*/
function Delete(value, connecteInfo) {
  // MySQLに接続
  var connection = Connect(connecteInfo);
  // idTable登録用データ宣言
  var idValue = [];
  // MySQLコマンドの作成
  var Query = 'DELETE FROM AddressTable where ';
  for(const index in value){
    if(index > 0){
      Query += ' or';
    }
    Query += (' id=' + value[index]);
    // idTable登録用データ作成
    idValue.push(['delete', value[index]]);
  }
  console.log(idValue);
  console.log(Query);
  // データの削除
  connection.query(Query, function (error, results, fields) { 
    console.log('Delete：' + results);
  });
  // MySQLとの接続を切断
  connection.end();

  // MySQLに接続(idTable用)
  var idConnect = Connect(connecteInfo);
  // MySQLコマンドの作成
  var idQuery = 'INSERT INTO idTable (name, id) VALUES ?';
  // 削除されたIDのデータをidTableに登録
  idConnect.query(idQuery, [idValue],function (error, r, fields) { 
    console.log('idInsert：' + r);
  });
  idConnect.end();
}

/*----------引数例----------*/

// MySQL情報の例
var info = {
  host     : 'localhost',
  user     : 'root',
  password : 'ys0718',
  database : 'FrankFurtDB'
};


// データ引き出し関数用の条件の値の例
var value = {
  name:'haru'
};
// PullData(value, info);

// データ登録用関数用の登録データの例
var data = {
  name:'tatsuya',
  mail:'okazaki@gmail.com',
  color:'black',
  flag:0
}
// Registration(data ,info);

// データ更新用関数用の更新データの例
var val = {
  id:'4',
  name:'yoshiharu'
}
// UpdateMail(val, info);

// データ削除関数用の条件の値の例
var v = [4, 6];
// Delete(v, info);