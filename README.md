Використання JSON-RPS API розглянемо на прикладі Postman: 
Прописуємо URL адресу `http://127.0.0.1:5000/api` і ставимо
метод запиту `POST` в заголовку запиту `headers` задаєм 
параметри Key:`Content-Type` value: `application/json` в тілі 
запиту вибираємо задання даних як `raw` та задаємо:<br>
`{`<br>
`  "jsonrpc": "2.0",`<br>
`  "method": "App.order_rpc",`<br>
`  "params": {"login": "your_login",`<br>
              `"password": "your_password", "order_id": order_id},`<br>
`  "id": 1`<br>
`}`

Замість `login` та `password` вставляємо логін та пароль який ви
створили при реєстрації на сайт. 

Приклад запиту:<br>
`{`<br>
`  "jsonrpc": "2.0",`<br>
`  "method": "App.order_rpc",`<br>
`  "params": {"login": "pashkevuchpasha@gmail.com",`<br>
`  "password": "qwe123", "order_id": 2},`<br>
`  "id": 42`<br>
`}`<br>

Відповідь: 
`{`<br>
`    "id": 1,`<br>
`    "jsonrpc": "2.0",`<br>
`    "result": {`<br>
`        "address": "Ukraine, Lviv, Saharova 11",`<br>
`        "amount": 1,`<br>
`        "id": 42,`<br>
`        "product": "Iphone",`<br>
`        "status": "Delivered"`<br>
`    }`<br>
`}`<br>