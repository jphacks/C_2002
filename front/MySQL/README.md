# MySQL

#### MySQL Setup
``` bash
$ mysql -u (user name) -p
Enter password: (password)

mysql> create database FrankFurtDB;

mysql> use FrankFurtDB;

mysql> create table AddressTable (id int unsigned not null, name varchar(100) not null, mail varchar(100) not null, color varchar(100), flag int);

mysql> desc AddressTable;

+-------+--------------+------+-----+---------+-------+
| Field | Type         | Null | Key | Default | Extra |
+-------+--------------+------+-----+---------+-------+
| id    | int unsigned | NO   |     | NULL    |       |
| name  | varchar(100) | NO   |     | NULL    |       |
| mail  | varchar(100) | NO   |     | NULL    |       |
| color | varchar(100) | YES  |     | NULL    |       |
| flag  | int          | YES  |     | NULL    |       |
+-------+--------------+------+-----+---------+-------+

mysql> create table idTable (name varchar(10), id int unsigned); 

mysql> desc idTable;

+-------+--------------+------+-----+---------+-------+
| Field | Type         | Null | Key | Default | Extra |
+-------+--------------+------+-----+---------+-------+
| name  | varchar(10)  | YES  |     | NULL    |       |
| id    | int unsigned | NO   |     | NULL    |       |
+-------+--------------+------+-----+---------+-------+

mysql> insert into idTable values ('next', 1);

mysql> SELECT * FROM idTable;

+------+----+
| name | id |
+------+----+
| next |  1 |
+------+----+

```


```javascript

// ----------引数例----------

// MySQL情報の例
let info = {
  host     : 'localhost',
  user     : 'root',
  password : 'ys0718',
  database : 'FrankFurtDB'
}


// データ引き出し関数用の条件の値の例
let value = {
  name:'haru'
}
// PullData(value, info)

// データ登録用関数用の登録データの例
let data = {
  name:'tatsuya',
  mail:'okazaki@gmail.com',
  color:'black',
  flag:0
}
// Registration(data ,info)

// データ更新用関数用の更新データの例
let val = {
  id:'4',
  name:'yoshiharu'
}
// UpdateMail(val, info)

// データ削除関数用の条件の値の例
let v = [4, 6]
// Delete(v, info)
```